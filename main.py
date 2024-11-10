import flet as ft
import pyperclip
import yt_dlp as youtube_dl
import pygame as pg
import os
from mutagen.mp3 import MP3
import asyncio

class song:
    def __init__(self, filename):
        self.filename = filename
        self.title = os.path.splitext(filename)[0]
        self.duration = self.get_duration()
        
    def get_duration(self): 
        audio = MP3(os.path.join('play', self.filename))
        return audio.info.length
    
async def apps(page: ft.Page):
    page.title = 'Salem'
    page.window.width = 320 # ancho
    page.window.height = 805 #Alto
    page.window.resizable = False  # Desactiva el cambio de tamaño de la ventana
    
    colors = ft.colors.ORANGE_900
    color_bg = ft.colors.BLACK

    # Campo de texto para el enlace
    link = ft.TextField(
        label='Link',
        border_radius=10,
        border_color=colors
    )
    
    # Mensaje de información
    info = ft.Text(value='', color=ft.colors.WHITE)
    
    def change(e):
        download.visible=False
        playeer.visible=False
        conf.visible=False
        if e == 0:
            download.visible=True
        elif e == 1:
            playeer.visible=True
        elif e == 2:
            conf.visible=True
        page.update()

                
    pg.mixer.init()
    playlist=[song(f) for f in os.listdir('play') if f.endswith('.mp3')]
    
    def load_song():
        pg.mixer.music.load(os.path.join('play', playlist[c_s_i].filename))
        
    def play_pause(e):
        if pg.mixer.music.get_busy():
            pg.mixer.music.pause()
            play_button.icon=ft.icons.PLAY_ARROW
        else:
            if pg.mixer.music.get_pos()==-1:
                load_song()
                pg.mixer.music.play()
            else:
                pg.mixer.music.unpause()
            play_button.icon=ft.icons.PAUSE
        page.update()
    
    def change_song(delta):
        nonlocal c_s_i
        c_s_i = (c_s_i + delta) % len(playlist)
        load_song()
        pg.mixer.music.play()
        update_info_song()
        play_button.icon = ft.icons.PAUSE
        page.update()

    
    def update_info_song():
        song = playlist[c_s_i]
        song_info.value=f'{song.title}'
        duracion.value=format_time(song.duration)
        prs_bar.value=0.0
        c_t_t.value='00:00'
        page.update()
        
    def format_time(seconds):
        m, s = divmod(int(seconds),60)
        return f'{m:02d}:{s:02d}'
    
    async def update_progress():
        while True:
            if pg.mixer.music.get_busy():
                current_time = pg.mixer.music.get_pos() / 1000  # Convert to seconds
                prs_bar.value = current_time / playlist[c_s_i].duration
                c_t_t.value = format_time(current_time)
                page.update()
            await asyncio.sleep(1)
        
    # Función para el botón "Pegar"
    def past(e):
        link.value = pyperclip.paste()
        link.update()

    # Función para descargar audio usando yt-dlp
    def downloadmV(e):
        if not link.value:
            info.value = 'No hay link'
            info.update()
        else:
            try:
                info.value = 'Descargando...'
                info.update()               
                ytlink = link.value.strip()
                ydl_opts = {
                    'format': 'bestaudio/best',  # Mejor calidad de audio
                    'postprocessors': [
                        {
                        'key': 'FFmpegExtractAudio',  # Usa FFmpeg para convertir el audio
                        'preferredcodec': 'mp3',  # Convierte a MP3
                        'preferredquality': '192',  # Calidad 192 kbps
                    }
                    ],
                    'ffmpeg_location': 'C:/ffmpeg',  # Aquí proporcionas la ruta a FFmpeg si es necesario
                    'outtmpl': './play/%(title)s.%(ext)s',  # Ruta y nombre de archivo de salida
                    
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([ytlink])
                info.value = 'Descargado exitosamente en MP3'
                link.value = ''
                link.update()
            except:
                info.value = 'Error al descargar'
                link.value = ''
                link.update()
            info.update()
    
    def play_song_from_list(index):
            nonlocal c_s_i
            c_s_i = index
            load_song()
            pg.mixer.music.play()
            update_info_song()
            play_button.icon = ft.icons.PAUSE
            page.update()

    c_s_i=0    
    song_info = ft.Text(size=10, color=ft.colors.WHITE)
    c_t_t = ft.Text(value='00:00', color=ft.colors.WHITE60,size=12)
    duracion = ft.Text(value='00:00', color=ft.colors.WHITE60, size=12)
    prs_bar = ft.ProgressBar(value=0.0, width=98, color=ft.colors.ORANGE_900, bgcolor='gray')
    play_button = ft.IconButton(icon=ft.icons.PLAY_ARROW, on_click=play_pause, icon_color=ft.colors.WHITE)
    before_button = ft.IconButton(icon=ft.icons.SKIP_PREVIOUS, on_click=lambda _: change_song(-1), icon_color=ft.colors.WHITE,)
    after_button = ft.IconButton(icon=ft.icons.SKIP_NEXT, on_click=lambda _: change_song(+1), icon_color=ft.colors.WHITE,)
    # Contenedor de descarga
    download = ft.Container(
        visible=True
        ,expand=True,
        content=ft.Column(
            controls=[
                link
                ,ft.Container(
                    height=50
                    ,content=ft.Column(
                        controls=[
                            ft.Text('Descarga')
                            ,info
                                    
                        ]
                    )
                )
                ,ft.Container(
                    expand=True,
                    content=ft.Column(
                        width=315,
                        alignment='end',
                        horizontal_alignment='end',
                        controls=[
                            ft.IconButton(
                                ft.icons.PASTE,
                                padding=4,
                                height=50,
                                width=60,
                                on_click=past
                            ),
                            ft.IconButton(
                                ft.icons.DOWNLOAD_SHARP,
                                padding=4,
                                height=50,
                                width=60,
                                on_click=downloadmV
                            )
                        ]
                    )
                ),
            ]
        )
    )

    playeer= ft.Container(
        visible=False
        ,expand=True
        ,content=ft.Column(
            expand=True
            ,controls=[
                ft.Column(
                    expand= True
                    ,scroll='auto'
                    ,controls=[
                        ft.Text('Reproductor')
                        ,ft.Column(
                            expand=True
                            ,controls=[
                                ft.Container(
                                on_click=lambda e, i=i: play_song_from_list(i)
                                ,width=310
                                ,border=ft.Border(left=ft.BorderSide(2, color=colors))
                                ,padding=10
                                ,bgcolor=ft.colors.with_opacity(0.2,ft.colors.BLUE_GREY_500)
                                ,content=ft.Text(song.title, color=ft.colors.WHITE,)
                                )
                                for i, song in enumerate(playlist)
                            ]
                        )
                    ]
                )
                ,ft.Container(
                    bgcolor='black'
                    ,border_radius=10
                    ,padding=5
                    ,content=ft.Row(
                        controls=[
                            ft.Container(
                                height=70
                                ,width=70
                                ,padding=8
                                ,border_radius=10
                                ,bgcolor=ft.colors.BLUE_GREY_500
                                ,content=ft.Icon(
                                    ft.icons.ALBUM
                                    ,size=50
                                )
                            )
                            ,ft.Column(
                                controls=[
                                    song_info
                                    ,ft.Row(
                                        controls=[
                                            c_t_t,
                                            prs_bar,
                                            duracion
                                        ]
                                    )
                                    ,ft.Row(
                                        alignment='center'
                                        ,controls=[
                                            before_button,
                                            play_button,
                                            after_button
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    )
    
    def thc(e):
        nonlocal colors
        themes = [ft.colors.ORANGE_900, ft.colors.BLUE_900, ft.colors.GREEN_900, ft.colors.YELLOW_900, ft.colors.PURPLE_900, ft.colors.RED_900]
        colors = themes[e] if e < len(themes) else colors
        page.update()
        
    conf = ft.Container(
        visible=False
        ,expand=True
        ,content=ft.Column(
            expand=True
            ,controls=[
                ft.Text('Temas')
                ,ft.Row(
                    col=12
                    ,alignment=ft.MainAxisAlignment.CENTER
                    ,controls=[
                            ft.Container(
                               height=50,
                               width=75,
                               padding=8
                               ,alignment=ft.alignment.center,
                               border_radius=10
                               ,bgcolor=ft.colors.ORANGE_900
                               ,on_click=lambda e: thc(0)
                               ,content=ft.Icon(ft.icons.CHECK)
                            ),
                            ft.Container(
                               height=50,
                               width=75,
                               padding=8
                               ,border_radius=10
                               ,bgcolor=ft.colors.BLUE_900
                               ,on_click=lambda e: thc(1)
                            ),
                            ft.Container(
                               height=50,
                               width=75,
                               padding=8
                               ,border_radius=10
                               ,bgcolor=ft.colors.GREEN_900
                               ,col=4)
                       ]
                    )
                ,ft.Row(
                    col=12
                    ,alignment=ft.MainAxisAlignment.CENTER
                    ,controls=[
                            ft.Container(
                               height=50,
                               width=75,
                               padding=8
                               ,alignment=ft.alignment.center,
                               border_radius=10
                               ,bgcolor=ft.colors.YELLOW_900
                            ),
                            ft.Container(
                               height=50,
                               width=75,
                               padding=8
                               ,border_radius=10
                               ,bgcolor=ft.colors.PURPLE_900
                            ),
                            ft.Container(
                               height=50,
                               width=75,
                               padding=8
                               ,border_radius=10
                               ,bgcolor=ft.colors.RED_900
                               ,col=4)
                       ]
                    )
            ]
        )
    )
    
    # Estructura principal de la interfaz
    page.add(
        ft.Container(
            width=310,
            height=750,
            border_radius=10,
            bgcolor=color_bg,
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Image(src='../assets/cat.svg', width=50, height=50, color=colors),
                            ft.Text('Salem', size=25, weight=ft.FontWeight.W_700)
                        ]
                    ),
                    ft.Divider(color=ft.colors.BLUE_GREY_900),
                    ft.Container(
                        expand=True,
                        content=ft.Stack(
                            expand=True
                            ,controls=[
                                download
                                ,playeer
                                ,conf
                            ]
                        )
                        
                    ),
                    ft.Container(
                        height=50,
                        border_radius=10,
                        content=ft.Row(
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.IconButton(
                                    ft.icons.HOME
                                    ,on_click=lambda e: change(0)
                                    ),
                                ft.IconButton(
                                    ft.icons.MUSIC_NOTE
                                    , on_click=lambda e: change(1)
                                    ),
                                ft.IconButton(
                                    ft.icons.SETTINGS
                                    ,on_click=lambda e: change(2)
                                    )
                            ]
                        )
                    )
                ]
            )
        )
    )
    if playlist:
        load_song()
        update_info_song()
        page.update()
        await update_progress()

ft.app(target=apps, assets_dir='assets')
