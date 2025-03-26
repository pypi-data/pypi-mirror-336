# -*- coding: utf-8 -*-
import libtorrent as lt
import requests
from colorama import init, Fore, Style
import os
import sys
import time
import urllib.parse
import base64
import threading
import signal
import argparse

init(autoreset=True)

class DownloadManager:
    def __init__(self):
        self.session = None
        self.tracker_index = 0
        self.original_trackers = []
        self.default_trackers = list(dict.fromkeys([
            "udp://tracker.opentrackr.org:1337/announce",
            "udp://tracker.openbittorrent.com:6969/announce",
            "udp://exodus.desync.com:6969/announce",
            "udp://tracker.torrent.eu.org:451/announce",
            "udp://open.stealth.si:80/announce",
            "http://tracker.files.fm:6969/announce",
        ]))
        self.web_trackers = self._fetch_trackers()
        self.all_trackers = []
        self.running = True
        self.lock = threading.Lock()
        os.makedirs("./downloads", exist_ok=True)
        self._init_session()
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, sig, frame):
        print(f"\n{Fore.YELLOW}➤ 收到退出信号{Style.RESET_ALL}")
        self.running = False
        if self.session:
            self.session.pause()
        sys.exit(0)

    def _fetch_trackers(self):
        sources = [
            "https://cf.trackerslist.com/best.txt",
            "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt",
            "https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/best.txt",
        ]
        trackers = set()
        for url in sources:
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                trackers.update(t.strip() for t in response.text.split('\n') if t.strip())
            except requests.RequestException as e:
                print(f"{Fore.YELLOW}⚠ 获取在线Tracker失败: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ 已加载 {len(trackers)} 个在线Tracker{Style.RESET_ALL}")
        return list(trackers)

    def _init_session(self):
        settings = {
            'download_rate_limit': 0,
            'upload_rate_limit':  0,
            'active_downloads': 8,
            'active_seeds': 4,
            'connections_limit': 2000,
            'connection_speed': 200,
            'enable_upnp': True,
            'enable_natpmp': True,
            'announce_to_all_tiers': True,
            'announce_to_all_trackers': True,
            'aio_threads': 16,
            'cache_size': 16384,
            'coalesce_reads': True,
            'coalesce_writes': True,
            'lazy_bitfields': True,
            'max_peerlist_size': 1000,
            'max_out_request_queue': 500,
            'enable_dht': True,
            'dht_announce_interval': 60,
            'enable_lsd': True,
            'listen_interfaces': '0.0.0.0:6881,[::]:6881'
        }
        self.session = lt.session(settings)

    def _switch_tracker(self, handle):
        with self.lock:
            if not self.all_trackers:
                print(f"{Fore.YELLOW}⚠ 无可用Tracker{Style.RESET_ALL}")
                return None
            self.tracker_index = (self.tracker_index + 1) % len(self.all_trackers)
            new_tracker = self.all_trackers[self.tracker_index]
            print(f"\n{Fore.YELLOW}➤ 切换Tracker: {new_tracker}{Style.RESET_ALL}")
            handle.add_tracker({'url': new_tracker, 'tier': 0})
            handle.force_reannounce()
            status = handle.status()
            print(f"{Fore.YELLOW}切换后状态: 种子:{status.num_seeds} 节点:{status.num_peers} ↓{self._human_readable_size(status.download_rate, 1)}/s{Style.RESET_ALL}")
            return status

    def _human_readable_size(self, size, decimal_places=2):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.{decimal_places}f}{unit}"
            size /= 1024.0
        return f"{size:.{decimal_places}f}PB"

    def _calculate_eta(self, rate, remaining):
        if rate <= 0:
            return "∞"
        seconds = int(remaining / rate)
        if seconds < 60:
            return f"{seconds}秒"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes}分{(seconds % 60):02d}秒"
        hours = minutes // 60
        return f"{hours}小时{(minutes % 60):02d}分"

    def decode_thunder_link(self, thunder_url):
        if thunder_url.startswith("thunder://"):
            try:
                encoded = thunder_url[10:]
                decoded = base64.b64decode(encoded).decode('utf-8')
                if decoded.startswith("AA") and decoded.endswith("ZZ"):
                    return decoded[2:-2]
                return decoded
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ 迅雷链接解码失败: {str(e)}{Style.RESET_ALL}")
                return None
        return thunder_url

    def parse_magnet_link(self, magnet_link):
        magnet_link = magnet_link.strip()
        is_thunder = magnet_link.startswith("thunder://")
        if is_thunder:
            magnet_link = self.decode_thunder_link(magnet_link)
            if not magnet_link:
                raise ValueError("迅雷链接解码失败")
        
        if not magnet_link.startswith("magnet:?"):
            if len(magnet_link) in (32, 40) and all(c in "0123456789abcdefABCDEF" for c in magnet_link):
                magnet_link = f"magnet:?xt=urn:btih:{magnet_link}"
            else:
                raise ValueError("无效的磁力链接或哈希值")
        
        params = dict(urllib.parse.parse_qs(urllib.parse.urlsplit(magnet_link).query))
        xt = params.get('xt', [''])[0]
        if not xt.startswith('urn:btih:'):
            raise ValueError("无法识别InfoHash")
        
        info_hash = xt.replace('urn:btih:', '')
        display_name = urllib.parse.unquote_plus(params.get('dn', [''])[0]) if params.get('dn') else None
        self.original_trackers = [urllib.parse.unquote(tr) for tr in params.get('tr', []) if tr]
        file_size = int(params.get('xl', ['0'])[0]) if params.get('xl') else None
        
        self.all_trackers = list(dict.fromkeys(self.original_trackers + self.default_trackers + self.web_trackers))
        effective_magnet = self._enhance_magnet(info_hash, display_name, file_size, self.all_trackers)
        
        print(f"{Fore.CYAN}➤ 增强后的磁力链接: {effective_magnet[:100]}{'...' if len(effective_magnet) > 100 else ''}{Style.RESET_ALL}")
        atp = lt.add_torrent_params()
        atp.url = effective_magnet
        atp.flags |= lt.torrent_flags.update_subscribe | lt.torrent_flags.auto_managed
        atp.save_path = "./downloads"
        atp.max_connections = 200
        atp.trackers = self.all_trackers
        
        resume_file = os.path.join("./downloads", f"{info_hash}.resume")
        if os.path.exists(resume_file):
            try:
                with open(resume_file, 'rb') as f:
                    resume_data = f.read()
                    if resume_data:
                        atp.resume_data = resume_data
                        print(f"{Fore.YELLOW}➤ 已加载续传数据{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}⚠ 续传数据为空，忽略{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ 加载续传数据失败: {str(e)}{Style.RESET_ALL}")
        
        try:
            handle = self.session.add_torrent(atp)
        except Exception as e:
            raise RuntimeError(f"添加种子失败: {str(e)}. 请检查libtorrent版本兼容性，可能需要更新至最新版")
        
        print(f"{Fore.CYAN}➤ 获取元数据 [{info_hash[:8]}...] 使用 {len(self.all_trackers)} 个Tracker{Style.RESET_ALL}", end="")
        
        start_time = time.time()
        max_duration = 180
        while not handle.status().has_metadata and time.time() - start_time < max_duration and self.running:
            print(".", end="", flush=True)
            time.sleep(1)
        
        if not handle.status().has_metadata:
            self.session.remove_torrent(handle)
            raise TimeoutError("元数据获取超时，请检查链接或网络")
            
        torrent_info = handle.torrent_file()
        files = [{'path': torrent_info.files().file_path(i), 'size': torrent_info.files().file_size(i), 'index': i}
                 for i in range(torrent_info.num_files())]
        
        print(f"\n{Fore.GREEN}✓ 元数据获取成功{Style.RESET_ALL}")
        
        return {
            'info_hash': info_hash,
            'name': display_name or torrent_info.name(),
            'total_size': torrent_info.total_size(),
            'total_size_human': self._human_readable_size(torrent_info.total_size()),
            'files': files,
            'effective_magnet': effective_magnet,
            'original_trackers': self.original_trackers,
            'torrent_info': torrent_info,
            'handle': handle
        }

    def _enhance_magnet(self, info_hash, display_name, file_size, trackers):
        magnet_link = f"magnet:?xt=urn:btih:{info_hash}"
        if display_name:
            magnet_link += f"&dn={urllib.parse.quote_plus(display_name)}"
        if file_size:
            magnet_link += f"&xl={file_size}"
        if trackers:
            magnet_link += ''.join(f'&tr={urllib.parse.quote(t)}' for t in trackers[:50])
        return magnet_link

    def _input_thread(self, handle=None):
        while self.running:
            try:
                cmd = input().strip().lower()
                if cmd == 'q':
                    print(f"{Fore.YELLOW}➤ 用户请求退出下载{Style.RESET_ALL}")
                    self.running = False
                elif cmd == 'x' and handle:
                    self._switch_tracker(handle)
            except EOFError:
                time.sleep(1)

    def download_torrent(self, parsed_info, selected_files=None):
        handle = parsed_info['handle']
        torrent_info = parsed_info['torrent_info']
        effective_magnet = parsed_info['effective_magnet']
        
        print(f"{Fore.YELLOW}➤ 初始化使用 {len(self.all_trackers)} 个Tracker{Style.RESET_ALL}")
        print(f"{Fore.CYAN}➤ 提示: 输入 'q' 退出下载，'x' 切换Tracker{Style.RESET_ALL}")
        
        total_size = torrent_info.total_size()
        num_files = torrent_info.num_files()
        file_priorities = [0] * num_files
        
        if selected_files is None:
            selected_files = list(range(num_files))
            selected_size = total_size
            for i in range(num_files):
                file_priorities[i] = 1
            print(f"{Fore.GREEN}✓ 下载全部文件 [{self._human_readable_size(total_size)}]{Style.RESET_ALL}")
        else:
            selected_size = sum(torrent_info.files().file_size(idx) for idx in selected_files if 0 <= idx < num_files)
            for idx in selected_files:
                if 0 <= idx < num_files:
                    file_priorities[idx] = 1
            print(f"{Fore.GREEN}✓ 下载 {len(selected_files)} 个文件 [{self._human_readable_size(selected_size)}]{Style.RESET_ALL}")
            
        handle.prioritize_files(file_priorities)
        piece_count = torrent_info.num_pieces()
        for i in range(piece_count):
            handle.piece_priority(i, 1)
            
        handle.set_download_limit(0)
        handle.set_upload_limit(0)
        handle.force_reannounce()
        
        input_thread = threading.Thread(target=self._input_thread, args=(handle,), daemon=True)
        input_thread.start()
        
        start_time = time.time()
        max_retries = 3
        retry_count = 0
        slow_start_time = None
        
        while retry_count < max_retries and self.running:
            download_timeout = 3600
            
            while time.time() - start_time < download_timeout and self.running:
                status = handle.status()
                downloaded = status.total_wanted_done
                progress = (downloaded / selected_size * 100) if selected_size > 0 else 0
                all_done = status.total_wanted_done >= status.total_wanted and downloaded >= selected_size
                
                bar_length = 60
                filled = int(progress / 100 * bar_length)
                bar = '█' * filled + '░' * (bar_length - filled)
                download_rate = self._human_readable_size(status.download_rate, 1)
                upload_rate = self._human_readable_size(status.upload_rate, 1)
                downloaded_size = self._human_readable_size(downloaded, 1)
                total = self._human_readable_size(selected_size, 1)
                eta = self._calculate_eta(status.download_rate, selected_size - downloaded)
                
                status_line = (
                    f"\r{Fore.CYAN}进度:{Style.RESET_ALL} [{Fore.GREEN}{bar}{Style.RESET_ALL}] {progress:.1f}% "
                    f"↓{Fore.GREEN if status.download_rate > 50000 else Fore.YELLOW}{download_rate}/s{Style.RESET_ALL} "
                    f"↑{upload_rate}/s 种子:{status.num_seeds} 节点:{status.num_peers} "
                    f"[{downloaded_size}/{total}] 剩余:{eta}"
                )
                sys.stdout.write(status_line[:170].ljust(170))
                sys.stdout.flush()
                
                if progress >= 99.9 or all_done:
                    print(f"\n{Fore.GREEN}✓ 下载完成: ./downloads/{torrent_info.name()}{Style.RESET_ALL}")
                    resume_file = os.path.join("./downloads", f"{parsed_info['info_hash']}.resume")
                    try:
                        handle.save_resume_data()
                        resume_data = None
                        resume_timeout = time.time() + 5
                        while resume_data is None and time.time() < resume_timeout and self.running:
                            alerts = self.session.pop_alerts()
                            for alert in alerts:
                                if isinstance(alert, lt.save_resume_data_alert):
                                    resume_data = alert.resume_data
                            time.sleep(0.1)
                        if resume_data:
                            with open(resume_file, 'wb') as f:
                                f.write(resume_data)
                            print(f"{Fore.GREEN}✓ 续传数据保存成功{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}⚠ 续传数据保存超时{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.YELLOW}⚠ 保存续传数据失败: {str(e)}{Style.RESET_ALL}")
                    
                    handle.force_recheck()
                    max_check_time = time.time() + 300
                    while handle.status().state in (lt.torrent_status.checking_files, lt.torrent_status.queued_for_checking) and time.time() < max_check_time and self.running:
                        time.sleep(1)
                    if handle.status().is_seeding:
                        print(f"{Fore.GREEN}✓ 文件验证成功{Style.RESET_ALL}")
                        self.session.remove_torrent(handle)
                        if os.path.exists(resume_file):
                            os.remove(resume_file)
                        return
                    else:
                        print(f"{Fore.YELLOW}⚠ 文件验证失败，可能已损坏{Style.RESET_ALL}")
                        retry_count += 1
                        if retry_count < max_retries:
                            print(f"{Fore.YELLOW}➤ 重试下载 ({retry_count}/{max_retries})...{Style.RESET_ALL}")
                            self.session.remove_torrent(handle)
                            atp = lt.add_torrent_params()
                            atp.url = effective_magnet
                            atp.save_path = "./downloads"
                            atp.flags |= lt.torrent_flags.auto_managed | lt.torrent_flags.update_subscribe
                            atp.max_connections = 200
                            atp.trackers = self.all_trackers
                            try:
                                handle = self.session.add_torrent(atp)
                            except Exception as e:
                                print(f"{Fore.RED}✗ 重试添加种子失败: {str(e)}{Style.RESET_ALL}")
                                return
                            handle.prioritize_files(file_priorities)
                            handle.force_reannounce()
                            start_time = time.time()
                        else:
                            print(f"{Fore.RED}✗ 下载失败: 文件验证失败超过最大重试次数{Style.RESET_ALL}")
                            self.session.remove_torrent(handle)
                            return
                
                if status.download_rate < 100 * 1024:
                    if slow_start_time is None:
                        slow_start_time = time.time()
                    elif time.time() - slow_start_time > 10:
                        self._switch_tracker(handle)
                        slow_start_time = None
                else:
                    slow_start_time = None
                
                time.sleep(1)
            retry_count += 1
            if retry_count < max_retries and self.running:
                print(f"{Fore.YELLOW}➤ 下载超时，重试 ({retry_count}/{max_retries})...{Style.RESET_ALL}")
                handle.force_reannounce()
                start_time = time.time()
        if not self.running:
            print(f"{Fore.YELLOW}➤ 下载已中断{Style.RESET_ALL}")
            self.session.remove_torrent(handle)

    def download_direct(self, url):
        print(f"{Fore.CYAN}➤ 开始直连下载: {url}{Style.RESET_ALL}")
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            file_name = os.path.basename(urllib.parse.urlsplit(url).path) or f"downloaded_{int(time.time())}"
            file_path = os.path.join("./downloads", file_name)
            
            if os.path.exists(file_path):
                print(f"{Fore.YELLOW}⚠ 文件已存在，跳过下载: {file_path}{Style.RESET_ALL}")
                return
            
            downloaded = 0
            start_time = time.time()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if not self.running:
                        print(f"{Fore.YELLOW}➤ 下载已中断{Style.RESET_ALL}")
                        os.remove(file_path)
                        return
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = (downloaded / total_size * 100) if total_size > 0 else 0
                        bar_length = 50
                        filled = int(progress / 100 * bar_length)
                        bar = '█' * filled + '░' * (bar_length - filled)
                        download_rate = self._human_readable_size(downloaded / (time.time() - start_time), 1)
                        downloaded_size = self._human_readable_size(downloaded, 1)
                        total_size_human = self._human_readable_size(total_size, 1) if total_size > 0 else "未知"
                        eta = self._calculate_eta(downloaded / (time.time() - start_time), total_size - downloaded) if total_size > 0 else "∞"
                        
                        status_line = (
                            f"\r{Fore.CYAN}进度:{Style.RESET_ALL} [{Fore.GREEN}{bar}{Style.RESET_ALL}] {progress:.1f}% "
                            f"↓{Fore.GREEN if downloaded / (time.time() - start_time) > 50000 else Fore.YELLOW}{download_rate}/s{Style.RESET_ALL} "
                            f"[{downloaded_size}/{total_size_human}] 剩余:{eta}"
                        )
                        sys.stdout.write(status_line[:150].ljust(150))
                        sys.stdout.flush()
            
            print(f"\n{Fore.GREEN}✓ 下载完成: {file_path}{Style.RESET_ALL}")
        except requests.RequestException as e:
            print(f"{Fore.RED}✗ 直连下载失败: {str(e)}{Style.RESET_ALL}")

def process_url(downloader, url):
    try:
        if not url:
            print(f"{Fore.YELLOW}⚠ 请输入有效的链接{Style.RESET_ALL}")
            return
        
        if url.lower() == 'q':
            print(f"{Fore.YELLOW}➤ 程序退出{Style.RESET_ALL}")
            downloader.running = False
            return
        
        if url.startswith("magnet:") or (len(url) in (32, 40) and all(c in "0123456789abcdefABCDEF" for c in url)):
            link_type = "torrent"
        elif url.startswith("thunder://"):
            link_type = "thunder"
        elif url.startswith(("http://", "https://")):
            link_type = "direct"
        else:
            link_type = "unknown"
            
        print(f"{Fore.CYAN}➤ 检测到类型: {link_type if link_type != 'unknown' else '未知类型'}{Style.RESET_ALL}")
        
        if link_type in ["torrent", "thunder"]:
            parsed_info = downloader.parse_magnet_link(url)
            print(f"\n{Fore.GREEN}╔════ 种子信息 ════╗{Style.RESET_ALL}")
            name_display = parsed_info['name'][:120] + '...' if len(parsed_info['name']) > 120 else parsed_info['name']
            print(f"{Fore.GREEN}║ 名称: {name_display}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}║ 哈希: {parsed_info['info_hash']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}║ 大小: {parsed_info['total_size_human']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}╚═══════════════════╝{Style.RESET_ALL}")
            
            if len(parsed_info['files']) > 1:
                print(f"\n{Fore.CYAN}📁 文件列表:{Style.RESET_ALL}")
                for i, file in enumerate(parsed_info['files']):
                    print(f"  [{Fore.YELLOW}{i}{Style.RESET_ALL}] {file['path'][:50]}{'...' if len(file['path']) > 50 else ''} [{downloader._human_readable_size(file['size'])}]")
                choice = input(f"{Fore.CYAN}➤ 选择操作: (a)全部下载, (s)选择文件, (n)跳过: {Style.RESET_ALL}").lower()
                if choice == 'a':
                    downloader.download_torrent(parsed_info)
                elif choice == 's':
                    indices_input = input(f"{Fore.CYAN}➤ 输入索引 (例如 0-2,4 或 单个数字): {Style.RESET_ALL}")
                    selected_files = []
                    for part in indices_input.split(','):
                        if '-' in part:
                            start, end = map(int, part.split('-'))
                            selected_files.extend(range(start, end + 1))
                        elif part.isdigit():
                            selected_files.append(int(part))
                    if selected_files and all(0 <= x < len(parsed_info['files']) for x in selected_files):
                        downloader.download_torrent(parsed_info, selected_files)
                    else:
                        print(f"{Fore.YELLOW}⚠ 未选择有效文件，跳过下载{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}➤ 已跳过当前下载{Style.RESET_ALL}")
            else:
                downloader.download_torrent(parsed_info, [0])
                print(f"{Fore.GREEN}✓ 检测到单个文件，默认下载{Style.RESET_ALL}")
        elif link_type == "direct":
            downloader.download_direct(url)
        else:
            print(f"{Fore.YELLOW}⚠ 不支持的链接类型: {url}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}✗ 处理失败: {str(e)}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}➤ 用户中断操作{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="XB下载器 - 支持磁力链接、迅雷链接和直连下载")
    parser.add_argument("url", nargs="?", help="磁力链接、迅雷链接或直连URL")
    args = parser.parse_args()

    print(f"{Fore.CYAN}╔════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║          XB下载器          {Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════╝{Style.RESET_ALL}")
    downloader = DownloadManager()

    if args.url:
        # 如果提供了命令行参数，直接处理链接
        process_url(downloader, args.url)
    else:
        # 否则进入交互模式
        while downloader.running:
            url = input(f"{Fore.CYAN}➤ 输入磁力链接、直链或迅雷链接 (q 退出): {Style.RESET_ALL}").strip()
            process_url(downloader, url)

if __name__ == "__main__":
    main()