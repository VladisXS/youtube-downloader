#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Downloader - Mobile Version
Мобільна версія для Android
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from pathlib import Path
import threading
import yt_dlp
import os

Window.size = (360, 640)


class YouTubeDownloaderApp(App):
    def build(self):
        self.title = "📺 YouTube Downloader"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Заголовок
        title_label = Label(
            text="📺 YouTube Downloader",
            size_hint_y=0.1,
            font_size='20sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(title_label)
        
        # Форма для введення
        form_layout = GridLayout(cols=1, spacing=10, size_hint_y=0.4)
        
        # Поле для посилання
        form_layout.add_widget(Label(text="Посилання на YouTube:", size_hint_y=None, height=40))
        self.url_input = TextInput(
            multiline=False,
            hint_text='https://youtu.be/...',
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.2, 0.2, 1)
        )
        form_layout.add_widget(self.url_input)
        
        # Поле для папки
        form_layout.add_widget(Label(text="Папка для завантаження:", size_hint_y=None, height=40))
        self.folder_input = TextInput(
            multiline=False,
            hint_text='YouTubeVladisX',
            text='YouTubeVladisX',
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.2, 0.2, 1)
        )
        form_layout.add_widget(self.folder_input)
        
        main_layout.add_widget(form_layout)
        
        # Кнопка для завантаження
        download_btn = Button(
            text='⬇️ Завантажити',
            size_hint_y=0.1,
            background_color=(0, 0.7, 0, 1)
        )
        download_btn.bind(on_press=self.download_video)
        main_layout.add_widget(download_btn)
        
        # Поле для логів
        log_scroll = ScrollView(size_hint_y=0.4)
        self.log_label = Label(
            text="📋 Статус:\n\nГотовий до завантаження...",
            size_hint_y=None,
            markup=True,
            text_size=(350, None),
            color=(1, 1, 1, 1),
            padding=(10, 10)
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        log_scroll.add_widget(self.log_label)
        main_layout.add_widget(log_scroll)
        
        return main_layout
    
    def update_log(self, message):
        """Оновлює лог повідомлення"""
        current = self.log_label.text
        self.log_label.text = f"{current}\n{message}"
    
    def download_video(self, instance):
        """Завантажує відео в окремому потоці"""
        url = self.url_input.text.strip()
        folder = self.folder_input.text.strip() or "YouTubeVladisX"
        
        if not url:
            self.log_label.text = "❌ Помилка: Введіть посилання!"
            return
        
        # Запуск завантаження в окремому потоці
        thread = threading.Thread(target=self._download, args=(url, folder))
        thread.daemon = True
        thread.start()
    
    def _download(self, url, folder):
        """Окремий потік для завантаження"""
        try:
            self.log_label.text = f"⏳ Завантаження починається...\n📂 Папка: {folder}\n\nОчікування..."
            
            # Створюємо папку
            download_path = Path(folder)
            download_path.mkdir(parents=True, exist_ok=True)
            
            # Налаштування для yt-dlp
            ydl_opts = {
                'format': '22/18/best',  # FullHD
                'outtmpl': str(download_path / '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': True,
            }
            
            # Завантажуємо
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            self.log_label.text = (
                f"✅ Успішно завантажено!\n"
                f"📄 Файл: {filename}\n"
                f"📂 Папка: {folder}"
            )
            
        except Exception as e:
            self.log_label.text = (
                f"❌ Помилка: {str(e)}\n\n"
                f"Перевірте:\n"
                f"• Посилання\n"
                f"• Інтернет\n"
                f"• Дозволи каналу"
            )


if __name__ == '__main__':
    YouTubeDownloaderApp().run()
