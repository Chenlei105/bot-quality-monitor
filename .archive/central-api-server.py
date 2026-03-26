#!/usr/bin/env python3
"""
中央数据收集 API 服务器

功能:
- 接收来自所有企业/机器人的匿名使用数据
- 写入飞书多维表格
- 支持跨企业访问（公开 API）

运行:
    python3 central-api-server.py

访问:
    http://localhost:8080/api/v1/usage
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys

# 飞书多维表格配置
BITABLE_APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
TABLE_ID = "tbllGdVAIIzITahT"

# 临时存储目录（写入飞书前缓存）
BUFFER_DIR = os.path.expanduser("~/.openclaw/workspace/logs/central-buffer")
os.makedirs(BUFFER_DIR, exist_ok=True)

class CentralAPIHandler(BaseHTTPRequestHandler):
    """处理数据上报请求"""
    
    def do_POST(self):
        """处理 POST 请求"""
        # 解析路径
        if self.path == "/api/v1/usage":
            self._handle_single_event()
        elif self.path == "/api/v1/usage/batch":
            self._handle_batch_events()
        else:
            self.send_error(404, "Not Found")
    
    def _handle_single_event(self):
        """处理单个事件上报"""
        try:
            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            event_data = json.loads(post_data.decode('utf-8'))
            
            # 验证数据格式
            required_fields = ["event_type", "skill_name", "user_id", "timestamp"]
            if not all(field in event_data for field in required_fields):
                self.send_error(400, "Missing required fields")
                return
            
            # 保存到缓冲区
            self._save_to_buffer([event_data])
            
            # 返回成功
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            
            print(f"[API] 收到事件: {event_data['event_type']} from {event_data['user_id']}")
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, str(e))
    
    def _handle_batch_events(self):
        """处理批量事件上报"""
        try:
            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            events = data.get("events", [])
            if not events:
                self.send_error(400, "No events provided")
                return
            
            # 保存到缓冲区
            self._save_to_buffer(events)
            
            # 返回成功
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "count": len(events)
            }).encode('utf-8'))
            
            print(f"[API] 收到批量事件: {len(events)} 条")
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, str(e))
    
    def _save_to_buffer(self, events):
        """保存事件到缓冲区"""
        import time
        buffer_file = os.path.join(BUFFER_DIR, f"buffer-{int(time.time())}.jsonl")
        
        with open(buffer_file, "w") as f:
            for event in events:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        
        print(f"[API] 已保存 {len(events)} 条到缓冲区: {buffer_file}")
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        pass  # 静默 HTTP 日志

def run_server(port=8080):
    """启动 API 服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CentralAPIHandler)
    
    print(f"=== 中央数据收集 API 服务器 ===")
    print(f"监听端口: {port}")
    print(f"API 端点: http://localhost:{port}/api/v1/usage")
    print(f"缓冲目录: {BUFFER_DIR}")
    print(f"目标表格: {BITABLE_APP_TOKEN}/{TABLE_ID}")
    print(f"\n按 Ctrl+C 停止服务器\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
