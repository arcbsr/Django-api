import os
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class FileUploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(self.upload_dir, exist_ok=True)
        self.chunks = {}
    
    async def disconnect(self, close_code):
        # Clean up if needed on disconnect
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # Receiving the file metadata and chunks
        if text_data:
            data = json.loads(text_data)
            if data.get('type') == 'start_upload':
                # Prepare for upload by initializing chunks for the given file
                file_name = data['file_name']
                self.chunks[file_name] = {
                    'current_chunk': 0,
                    'total_chunks': data['total_chunks'],
                    'file_path': os.path.join(self.upload_dir, file_name),
                }
                print(f"Started receiving {file_name}")
        
        if bytes_data:
            # Handle the file chunk
            # file_name = self.scope['url_route']['kwargs']['file_name']
            # chunk_info = self.chunks.get(file_name)
            for file_name, chunk_info in list(self.chunks.items()):
                
                    with open(chunk_info['file_path'], 'ab') as f:
                        f.write(bytes_data)

                    # Update chunk count
                    chunk_info['current_chunk'] += 1

                    # Check if all chunks are received
                    if chunk_info['current_chunk'] == chunk_info['total_chunks']:
                        # File is fully uploaded
                        del self.chunks[file_name]
                        await self.send(json.dumps({
                            'type': 'upload_complete',
                            'file_name': file_name,
                            'file_path': chunk_info['file_path'],
                        }))
                        print(f"Upload complete for {file_name}")
                    else:
                        # Acknowledge the receipt of the current chunk
                        await self.send(json.dumps({
                            'type': 'chunk_received',
                            'file_name': file_name,
                            'chunk_number': chunk_info['current_chunk'],
                        }))
