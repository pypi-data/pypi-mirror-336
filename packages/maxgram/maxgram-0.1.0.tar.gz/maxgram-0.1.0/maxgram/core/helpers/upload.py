import os
from typing import Any, Dict, Optional, TypedDict, Union

import aiohttp

class UploadOptions(TypedDict, total=False):
    """
    Базовые опции для загрузки файлов
    """
    path: str
    url: str
    file: Any
    
class UploadFileOptions(UploadOptions):
    """
    Опции для загрузки файлов
    """
    filename: Optional[str]
    
class UploadImageOptions(UploadOptions):
    """
    Опции для загрузки изображений
    """
    width: Optional[int]
    height: Optional[int]
    
class UploadVideoOptions(UploadOptions):
    """
    Опции для загрузки видео
    """
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]
    
class UploadAudioOptions(UploadOptions):
    """
    Опции для загрузки аудио
    """
    duration: Optional[int]
    title: Optional[str]
    performer: Optional[str]

class Upload:
    """
    Класс для загрузки файлов
    """
    
    def __init__(self, api):
        self.api = api
    
    async def image(self, options: UploadImageOptions) -> Dict[str, Any]:
        """
        Загружает изображение
        """
        return await self._upload('image', options)
    
    async def video(self, options: UploadVideoOptions) -> Dict[str, Any]:
        """
        Загружает видео
        """
        return await self._upload('video', options)
    
    async def audio(self, options: UploadAudioOptions) -> Dict[str, Any]:
        """
        Загружает аудио
        """
        return await self._upload('audio', options)
    
    async def file(self, options: UploadFileOptions) -> Dict[str, Any]:
        """
        Загружает файл
        """
        return await self._upload('file', options)
    
    async def _upload(self, type_: str, options: UploadOptions) -> Dict[str, Any]:
        """
        Загружает файл указанного типа
        """
        if 'url' in options:
            return await self._upload_by_url(type_, options['url'], options)
            
        if 'path' in options:
            return await self._upload_by_path(type_, options['path'], options)
            
        if 'file' in options:
            return await self._upload_file(type_, options['file'], options)
            
        raise ValueError('Необходимо указать url, path или file для загрузки')
    
    async def _upload_by_url(self, type_: str, url: str, extra: Dict[str, Any]) -> Dict[str, Any]:
        """
        Загружает файл по ссылке
        """
        params = {k: v for k, v in extra.items() if k not in ['url', 'path', 'file']}
        
        response = await self.api.raw.files.upload_by_url({
            'type': type_,
            'url': url,
            **params
        })
        
        return response.get('file', {})
    
    async def _upload_by_path(self, type_: str, path: str, extra: Dict[str, Any]) -> Dict[str, Any]:
        """
        Загружает файл с диска
        """
        filename = extra.get('filename', os.path.basename(path))
        
        with open(path, 'rb') as file:
            return await self._upload_file(type_, file, {**extra, 'filename': filename})
    
    async def _upload_file(self, type_: str, file: Any, extra: Dict[str, Any]) -> Dict[str, Any]:
        """
        Загружает файл из объекта файла
        """
        filename = extra.get('filename', 'file')
        params = {k: v for k, v in extra.items() if k not in ['url', 'path', 'file', 'filename']}
        
        # Получение URL для загрузки
        upload_url_response = await self.api.raw.files.get_upload_url({
            'type': type_,
            'filename': filename,
            **params
        })
        
        upload_url = upload_url_response.get('upload_url')
        
        if not upload_url:
            raise RuntimeError('Не удалось получить URL для загрузки файла')
        
        # Загрузка файла
        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            form.add_field('file', file, filename=filename)
            
            async with session.post(upload_url, data=form) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(f'Ошибка при загрузке файла: {error_text}')
                
                result = await response.json()
                return result.get('file', {}) 