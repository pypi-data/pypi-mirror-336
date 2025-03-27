
import uuid
import io


class MultipartFormBuilder:
    def __init__(self, boundary=None):
        """
        初始化 multipart/form-data 构建器
        
        Args:
            boundary: 自定义 boundary 字符串（可选）
        """
        self.boundary = boundary or f'----MultipartFormBoundary{uuid.uuid4().hex}'
        self.parts = []
    
    def add_field(self, name, value):
        """添加普通表单字段"""
        headers = {
            'Content-Disposition': f'form-data; name="{name}"'
        }
        content = str(value)
        
        self.parts.append({
            'headers': headers,
            'content': content
        })
        return self
    
    def add_file(self, name, filename, content, content_type=None):
        """
        添加文件
        
        Args:
            name: 表单字段名
            filename: 文件名
            content: 文件内容（bytes）
            content_type: 内容类型（可选）
        """
        headers = {
            'Content-Disposition': f'form-data; name="{name}"; filename="{filename}"'
        }
        
        if content_type:
            headers['Content-Type'] = content_type
        
        self.parts.append({
            'headers': headers,
            'content': content,
            'is_binary': True
        })
        return self
    
    def get_content_type(self):
        return f'multipart/form-data; boundary={self.boundary}'
    
    def build(self):
        """构建 multipart/form-data 请求体"""
        lines = []
        
        for part in self.parts:
            # 边界
            lines.append(f'--{self.boundary}'.encode())
            
            # 头部
            for header_name, header_value in part['headers'].items():
                lines.append(f'{header_name}: {header_value}'.encode())
            
            # 空行分隔头部和内容
            lines.append(b'')
            
            # 内容
            if part.get('is_binary', False):
                if isinstance(part['content'], bytes):
                    lines.append(part['content'])
                else:
                    lines.append(str(part['content']).encode())
            else:
                lines.append(str(part['content']).encode())
        
        # 结束边界
        lines.append(f'--{self.boundary}--'.encode())
        
        # 使用 CRLF 连接
        return b'\r\n'.join(lines)
    
    def get_headers(self):
        return {
            'Content-Type': self.get_content_type()
        }
