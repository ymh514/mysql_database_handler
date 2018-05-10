class Dictionary:
    type_tablename_dict = {
        'image': 'image',
        'video': 'video',
        'music': 'music',
        'file': 'file',
        'folder': 'folder'}
    type_dict = {
        'mp3': 'music',
        'aac': 'music',
        'flac': 'music',
        'ogg': 'music',
        'wma': 'music',
        'm4a': 'music',
        'aiff': 'music',
        'wav': 'music',
        'amr': 'music',
        'flv': 'video',
        'ogv': 'video',
        'avi': 'video',
        'mp4': 'video',
        'mpg': 'video',
        'mpeg': 'video',
        '3gp': 'video',
        'mkv': 'video',
        'ts': 'video',
        'webm': 'video',
        'vob': 'video',
        'wmv': 'video',
        'png': 'image',
        'jpeg': 'image',
        'gif': 'image',
        'jpg': 'image',
        'bmp': 'image',
        'svg': 'image',
        'webp': 'image',
        'psd': 'image',
        'tiff': 'image',
        'txt': 'file',
        'pdf': 'file',
        'doc': 'file',
        'docx': 'file',
        'odf': 'file',
        'xls': 'file',
        'xlsv': 'file',
        'xlsx': 'file',
        'ppt': 'file',
        'pptx': 'file',
        'ppsx': 'file',
        'odp': 'file',
        'odt': 'file',
        'ods': 'file',
        'md': 'file',
        'json': 'file',
        'csv': 'file',
        }

    def get_file_type(self, file_extension):
        """ Return file extension's type """
        return_str = ""
        if file_extension in self.type_dict:
            return_str = self.type_dict[file_extension]
        else:
            return_str = 'file'

        return return_str