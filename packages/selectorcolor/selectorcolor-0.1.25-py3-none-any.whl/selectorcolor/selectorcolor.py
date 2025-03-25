import flet as ft
from time import sleep
from pickle import dump, load
from os import path

class SelectorColor(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True
        self.width = 800
        self.border_radius = 15
        self.border = ft.border.all(1, "grey800")
        self.alignment = ft.alignment.top_center
        self.padding = 20
        self.GetArquivo()

        self.slides = {
            l: ft.Slider(
                min=0, 
                max=255, 
                value=0,
                height=30, 
                width=305,                
                active_color="#00ADFF",
                thumb_color ="#00ADFF",
                inactive_color="#205049",
                on_change=self.update_color,  
                overlay_color = 'trasparent',
                col = 11,   
                expand=True,            
            ) 
            for l in ['r', 'g', 'b']
        }

        self.titulo = ft.Text(
            value="Título", 
            selectable=True,
            size = 30, 
            weight= 'BOLD', 
            color = '#ffffff'
        )
        self.texto1 = ft.Text(
            value="Texto 1", 
            selectable=True,
            size = 15, 
            # weight= 'BOLD', 
            color = '#ffffff'
        )
        self.texto2 = ft.Text(
            value="Texto 2", 
            selectable=True,
            size = 12, 
          
            color = '#ffffff'
        )                
        self.color_text = ft.Text(
            value="Texto", 
            selectable=True,
            size = 20, 
            weight= 'BOLD', 
            # color = '#ffffff'
        )
        self.color_box = ft.Container(
            content = self.color_text, 
            width=100, 
            height=100, 
            bgcolor="#ff0000", 
            border_radius=12,
            alignment=ft.alignment.center,
           
        )
        self.botao = ft.ElevatedButton(
            text="Botão",
            width=100,
        ) 
               
        self.color_box2 = ft.Container(
            content=ft.Column(
                controls = [
                    self.titulo,
                    ft.Divider(10, color='transparent'),
                    ft.Row([self.color_box,self.botao], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    ft.Row([self.texto1,self.texto2], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                   
                ],
                horizontal_alignment='center',
                alignment='center',
                # tight=True,
                spacing= 3,
                expand=True,
            ),
            alignment=ft.alignment.center,
            width=260, 
            height=210, 
            border_radius=12,
            bgcolor="#0000ff",
            expand_loose=True,
            col =  {'xs':12, 'sm':5},

            )
        

        
        self.gradiente = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#000000", "#000000"],
        )
        self.sombras = ft.BoxShadow(spread_radius=0, blur_radius=20, color='black')        

        self.ativar_sombras = ft.Checkbox(label="Ativar Sombras", label_style = ft.TextStyle(color = "#BEBCE7"),value =False, on_change=self.GerenciarSombras)
        self.ativar_gradiente = ft.Checkbox(label="Ativar Gradiente", label_style = ft.TextStyle(color = "#BEBCE7"),value =False, on_change=self.GerenciarGradiente)
        self.ativar_bordas = ft.Checkbox(label="Ativar Bordas", label_style = ft.TextStyle(color = "#BEBCE7"),value =False, on_change=self.GerenciarBordas)

        self.color_scheme=ft.ColorScheme()
        self.text_theme = ft.TextStyle(color=None)
        self.datas = {
            "Container": lambda color: setattr(self.color_box, 'bgcolor', color), 
            "Fundo": self.ChangeFundoColor,
            "Texto": lambda color: setattr(self.color_text, 'color', color),
            "Título": lambda color: setattr(self.titulo, 'color', color),
            "Texto 1": lambda color: setattr(self.texto1, 'color', color),
            "Texto 2": lambda color: setattr(self.texto2, 'color', color),
            "Bordas": self.ChangeBordasColor,
            "Sombras": self.ChangeSombrasColor,
            "Gradiente": self.ChangeGradienteColor, 
            "Botão": lambda color: setattr(self.botao, 'bgcolor', color),
            "primary":  lambda color: setattr(self.color_scheme, 'primary', color),
            "on_primary":  lambda color: setattr(self.color_scheme, 'on_primary', color),
            "on_secondary_container":  lambda color: setattr(self.color_scheme, 'on_secondary_container', color),
            "outline":  lambda color: setattr(self.color_scheme, 'outline', color),
            "shadow":  lambda color: setattr(self.color_scheme, 'shadow', color),
            "on_surface_variant":  lambda color: setattr(self.color_scheme, 'on_surface_variant', color),
            "surface_variant":  lambda color: setattr(self.color_scheme, 'surface_variant', color),
            "primary_container":  lambda color: setattr(self.color_scheme, 'primary_container', color),
            "on_surface":  lambda color: setattr(self.color_scheme, 'on_surface', color),
            "surface":  lambda color: setattr(self.color_scheme, 'surface', color),
        }


        legenda = {
            'primary': 'texto principal, fundo filledbutton, texto outlinedbutton, slider true,  preenchimento do switch, checkbox True, icone,  texto do elevatebuton',
            'on_primary': 'texto filledbutton e bolinha do swicth com True',
            'on_secondary_container': 'texto filledtonalbutton',
            'outline': 'borda do outliedbutton',
            'shadow': 'sombras',
            'on_surface_variant': 'labels, hint do texfied, caixa do checkbox, check do popMenubutton, bolinha False do switch',
            'surface_variant': 'slider false, fundo do texfield e do dropdown quando filled = true, switch false',
            'primary_container': ' HOVERED da bolinha do switch',
            'on_surface': 'HOVERED do checkbox,items do popmenubuton, borda do Dropdown',
            'surface': 'fundo',
            "surface_container_low":  'fundo do card',
            "outline_variant":'divider',
            "secondary_container": 'prograss_bar False',
            "Boddy_large": 'Texto do TextField e Dropdown quando dense = true',
            "Boddy_medium": 'Texto do TextField e Dropdown quando dense = false',
  

        }

        self.tabela_legenda = ft.Column(
            controls = [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(i, weight='BOLD',width=160,text_align='center', color="#CADCBA"),
                            ft.VerticalDivider(10, color='primary,0.5'),
                            ft.Text(legenda[i],width=220,color="#BEBCE7", expand=True),
                        ],
                        spacing=0,
                    ),
                    expand = True,
                    
                    border=ft.border.all(1, 'white,0.5'),
                )
                for i in legenda.keys()
           
            ],
            spacing=0,
            run_spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
            # width=400,
            visible=False,
            expand=True,
        )

        self.objetos = ft.Dropdown(
            width=350,
            # menu_width =200,
            options=[ft.dropdown.Option(i) for i in self.datas.keys()],
            hint_text="Selecione o objeto",
            dense=True,
            filled=True,
            fill_color='grey900',
            border_color='grey800',
            border_width=1,
            border_radius=15,
            on_change=self.SetObjeto,
            enable_filter = True,
            enable_search = True,
            editable=True,
            col = 11,            
        )
      

     

        self.cor = 'black'

        self.btn_exportar_cores = ft.ElevatedButton(
            text="Exportar",
            tooltip="Exportar as cores \npara área de transferência",
            on_click=self.ExportarCores,
            bgcolor='grey800',
            color="#B0B3B1",
            col = {'xs':12, 'sm':4},
        )
        self.btn_save = ft.FilledButton(
            'Salvar Tema', 
            bgcolor='grey800', 
            on_click=self.TornarVizivel,
            color="#B0B3B1"
        )
        self.nome_tema = ft.TextField(
            hint_text='Digite o nome do tema',
            hint_style=ft.TextStyle(color='grey300'),
            text_style=ft.TextStyle(color='grey300'),
            col=96,
            border_width=1,
            border_color='grey800',
            border_radius=15,
            fill_color='grey900',
            filled=True,
            dense=True,
            content_padding=ft.Padding(5, 0, 0, 25),
            height=40,
            visible=False,
            expand=True,
            suffix=ft.Row(
                [
                    ft.IconButton(ft.Icons.SAVE,  tooltip='Confirmar', on_click=self.Salvar,icon_color='grey600'),
                    ft.IconButton(ft.Icons.CANCEL,on_click=self.Cancelar,icon_color='grey600',tooltip='Cancelar'),
                ],
                spacing=0,
                tight=True,
            )
        )    


        self.tema_escolhido = ft.Dropdown(
            hint_text='Selecione um tema',
            hint_style=ft.TextStyle(color='grey300'),         
            width=500,
            # menu_width = 200,
            
            dense=True,
            filled=True,
            fill_color='grey900', 
            border_color='grey800',
            border_radius=15, 
            border_width=1,
            col ={'xs':12, 'sm':8},
            expand=True,         
            
            options = [
                ft.dropdown.Option(i)
                for i in sorted(list(self.arquiv.keys()))
            ],
            on_change=self.CarregarTema
        )

        """
        xs	<576px
        sm	≥576px
        md	≥768px
        lg	≥992px
        xl	≥1200px
        xxl ≥1400px
        """
        cols = {
            "xs": 24,"sm": 24,"md": 24,
            "lg": 24,"xl": 24,"xxl": 24,
        }
        self.exibir_legendas = ft.Checkbox(
            label="Exibir legendas" if not self.tabela_legenda.visible else "Ocultar legendas",
            label_style = ft.TextStyle(color = "#BEBCE7"),
            # fill_color = 'grey500,0.1',
            # border_side = ft.border.all(5, ft.Colors.BLUE),
            # check_color = 'white',
            # active_color = 'white',
            on_change=self.ExibirLegendas,
            value=False,
        )
        self.icone_copy  = ft.IconButton(
            icon=ft.Icons.COPY, 
            icon_size = 10,                                       
            splash_radius=0,
            icon_color='white',
            on_click=lambda e: e.page.set_clipboard(f'"{self.cor}"'),
            col = 1,
        )
        self.controles = ft.Container(
            content = ft.Column(
                [
                    ft.ResponsiveRow(
                        [
                            self.ativar_sombras, 
                            self.ativar_bordas, 
                            self.ativar_gradiente,
                            self.exibir_legendas,
                        ], 
                        alignment='center', 
                        spacing=1,
                        run_spacing=1,
                        # wrap=False
                        columns=24,
                    ),
                    ft.ResponsiveRow(
                            [
                            self.ContainerHover(self.objetos),
                            self.icone_copy
                        ], 
                        spacing = 0,
                        
                                                            
                    ),                                    
                    ft.Stack(
                        controls = [
                            ft.Text("R", selectable=True, color="#BEBCE7", col = 1, left = 0,top = 2,),ft.Container(self.slides[f'r'],left = 5,top = 0),
                            ft.Text("G", selectable=True, color="#BEBCE7", col = 1, left = 0,top = 27),ft.Container(self.slides[f'r'],left = 5,top = 25),
                            ft.Text("B", selectable=True, color="#BEBCE7", col = 1, left = 0,top = 52),ft.Container(self.slides[f'r'],left = 5,top = 50),
                            
                        ], 
                        alignment=ft.alignment.center,
                        expand=True,
                        # width=380,
                        height=80,
                    ),

                ],
                width=380,
                spacing=0,
                run_spacing=0,
                horizontal_alignment='center',
                tight=True,
                # scroll=ft.ScrollMode.ADAPTIVE,
                # expand=True,
            ),
            border=ft.border.all(1, 'grey800'),
            border_radius=15,
            padding=20,
            expand_loose=True,
            col =  {'xs':12, 'sm':7}
            # height=400,
        )

        self.content = ft.Column(
            controls = [
                ft.ResponsiveRow(
                    controls = [
                        self.color_box2,
                        self.controles,
                        
                        ft.ResponsiveRow(
                            [self.btn_exportar_cores, self.tema_escolhido], 
                            alignment='center', 
                            vertical_alignment='center'                                                      
                        ),
                        ft.ResponsiveRow(
                            [self.btn_save,self.nome_tema,]
                            , alignment='center',                           
                        ),
                         
                        self.tabela_legenda,                   
                    ],
                    alignment='center', 
                    columns=12
                
                ),                                                                                                                            
            ], 
            # alignment='center',
            horizontal_alignment='center',
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,  
        )


    def ContainerHover(self, componente):
        def Hover(e):
            if e.data == 'true':
                componente.scale = 1.05
                componente.bgcolor = 'grey700'
                
            else:
                componente.scale = 1
                componente.bgcolor = 'grey800'
                
            componente.update()
        
        return ft.Container(
            content = componente,
            on_hover = Hover,
            col = componente.col
        )



    def ExibirLegendas(self, e):
        self.tabela_legenda.visible = e.control.value
        self.tabela_legenda.update()
        e.control.label = "Exibir legendas" if not self.tabela_legenda.visible else "Ocultar legendas"
        e.control.update()
        self.update()

    def Cancelar(self, e):
        self.nome_tema.clean()
        self.nome_tema.visible = False
        self.nome_tema.update()
        self.btn_save.visible = True
        self.update()


    def Salvar(self, e):
        nome_tema = self.nome_tema.value
        if nome_tema not in ['', ' ', None]:#+list(self.arquiv.keys()):
            self.GetArquivo()
            self.arquiv[nome_tema] = self.dic
            self.SalvarPickle(self.arquiv, self.nome_temas)

            self.nome_tema.visible = False
            self.btn_save.visible = True
            self.tema_escolhido.options.append(ft.dropdown.Option(nome_tema))
            self.tema_escolhido.update()
            self.pprint('tema salvo com sucesso!')
        else:
            self.nome_tema.hint_text = 'Digite um nome de Tema válido ou clique em Cancelar'
            # self.nome_tema.hint_style = ft.TextStyle(size = 10)

        self.update()


    def TornarVizivel(self, e):
        self.btn_save.visible = False
        self.nome_tema.visible = True
        self.nome_tema.update()
        self.btn_save.update()

    def ExportarCores(self, e):
        cores =f'''
cores = {{  
    "Container": "{self.color_box.bgcolor}",
    "Fundo":"{self.color_box2.bgcolor}",
    "Texto": "{self.color_text.color}",
    "Título": "{self.titulo.color}",
    "Texto 1": "{self.texto1.color}",
    "Texto 2": "{self.texto2.color}",
    "Bordas": "{self.sombras.color}",
    "Sombras": "{self.sombras.color}",
    "Gradiente": "{self.gradiente.colors[0]}","{self.gradiente.colors[1]}",
    "Botão":"{self.botao.bgcolor}",
    "primary":  "{self.color_scheme.primary}",
    "on_primary":  "{self.color_scheme.on_primary}",
    "on_secondary_container":  "{self.color_scheme.on_secondary_container}",
    "outline": " {self.color_scheme.outline}",
    "shadow":  "{self.color_scheme.shadow}",
    "on_surface_variant":  "{self.color_scheme.on_surface_variant}",
    "surface_variant":  "{self.color_scheme.surface_variant}",
    "primary_container":  "{self.color_scheme.primary_container}",
    "on_surface":  "{self.color_scheme.on_surface}",
    "surface":  "{self.color_scheme.surface}",
}}
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary = cores["primary"],
                on_primary = cores["on_primary"],
                on_secondary_container = cores["on_secondary_container"],
                outline = cores["outline"],
                shadow = cores["shadow"],
                on_surface_variant = cores["on_surface_variant"],
                surface_variant = cores["surface_variant"],
                primary_container = cores["primary_container"],
                on_surface = cores["on_surface"],
                surface = cores["surface"],
            )
            text_theme = ft.TextTheme(
                body_medium=cores["Texto"]  # Cor do texto padrão
            )   
        )    
    '''
        self.page.set_clipboard(cores)

    def ChangeBordasColor(self, color):
        if self.ativar_bordas.value:
            self.bordas = ft.border.all(1, color)
            setattr(self.color_box, 'border', self.bordas)
            self.color_box.update()
            self.update()

    def ChangeSombrasColor(self, color):
        if self.ativar_sombras.value:
            self.sombras.color = color
            setattr(self.color_box, 'shadow', self.sombras)
            self.color_box.update()
            self.update()


    def ChangeGradienteColor(self, color):
        if self.ativar_gradiente.value:
            self.gradiente.colors[1] = color
            setattr(self.color_box2, 'gradient', self.gradiente)
            self.color_box2.update()
            self.update()

    def ChangeFundoColor(self, color):
        if not self.ativar_gradiente.value:
            setattr(self.color_box2, 'bgcolor', color)
        else:
            self.gradiente.colors[0] = color
            setattr(self.color_box2, 'gradient', self.gradiente)
        setattr(self.color_scheme, 'surface', color)            
        self.color_box2.update()
        self.update()


    def SetObjeto(self, e):
        self.slides['r'].data = e.control.value
        self.slides['g'].data = e.control.value
        self.slides['b'].data = e.control.value

        self.SetColorFromHex(self.dic.get(e.control.value,"#000000"))


    def SetColorFromHex(self, hex_color):
        # Remove o caractere '#' se presente
        hex_color = hex_color.lstrip('#')
        
        # Converte os valores hexadecimais para inteiros
        r_value = int(hex_color[0:2], 16)
        g_value = int(hex_color[2:4], 16)
        b_value = int(hex_color[4:6], 16)
        
        # Seta os valores dos slides
        self.slides['r'].value = r_value
        self.slides['g'].value = g_value
        self.slides['b'].value = b_value
        
        # Atualiza a cor e os valores exibidos
        self.cor = f'#{r_value:02X}{g_value:02X}{b_value:02X}'
        self.R.value = f'R ({r_value:02})'
        self.G.value = f'G ({g_value:02})'
        self.B.value = f'B ({b_value:02})'

        self.update()

        
        # Atualiza os valores anteriores dos slides
        self.prev_r = r_value
        self.prev_g = g_value
        self.prev_b = b_value


    def GerenciarSombras(self, e):
        if self.ativar_sombras.value:
            self.color_box.shadow = self.sombras
        else:
            self.color_box.shadow = None
        # self.sombras.visible = self.ativar_sombras.value
        self.SetValueCLienStorage(f'{self.ativar_sombras.value}', "Ativar Sombras")
        self.dic["Ativar Sombras"] = self.ativar_sombras.value
        self.color_box.update()
        self.update()

    def GerenciarGradiente(self, e):
        if self.ativar_gradiente.value:
            # cor = self.GetColorSafe('Gradiente') or 'blue'
            if self.color_box2.bgcolor == None:
                self.color_box2.bgcolor = 'black'
            if self.gradiente.colors[1] == None:
                self.gradiente.colors[1] = self.color_box2.bgcolor
            self.gradiente.colors[0] = self.color_box2.bgcolor
            # print(self.gradiente.colors)
            self.color_box2.gradient = self.gradiente
        else:
            self.color_box2.gradient = None
        # self.gradiente.visible = self.ativar_gradiente.value
        self.SetValueCLienStorage(f'{self.ativar_gradiente.value}', "Ativar Gradiente")
        self.dic["Ativar Gradiente"] = self.ativar_gradiente.value
        self.color_box2.update()
        self.update()

    def GerenciarBordas(self, e):
        if self.ativar_bordas.value:
            self.color_box.border = self.bordas
        else:
            self.color_box.border = None
        # self.bordas.visible = self.ativar_bordas.value
        self.SetValueCLienStorage(f'{self.ativar_bordas.value}', "Ativar Bordas")
        self.dic["Ativar Bordas"] = self.ativar_bordas.value
        self.color_box.update()
        self.update()

    def update_color(self, e):
        if e.control.data:
            self.cor = f'#{int(self.slides['r'].value):02X}{int(self.slides['g'].value):02X}{int(self.slides['b'].value):02X}'

            self.datas[e.control.data](self.cor)
            self.update()
            self.page.update()
            self.SetValueCLienStorage(f'{self.page.title}_{e.control.data}', self.cor)
            self.dic[e.control.data] = self.cor


    def SetValueCLienStorage(self, key, value, retries=3, delay=1):
        for attempt in range(retries):
            try:
                self.page.client_storage.set(key, value)
                return
            except TimeoutError as e:
                if attempt < retries - 1:
                    print(f"Tentativa {attempt + 1} falhou. Tentando novamente após {delay} segundos...")
                    sleep(delay)
                else:
                    raise e

    def GetColorSafe(self, key):
        if __name__ == '__main__':
            v =  self.page.client_storage.get(f'{self.page.title}_{key}') or None            
        else:
            v= None
        return v

    def did_mount(self):
        self.titulo.color = self.GetColorSafe('Título')
        self.texto1.color = self.GetColorSafe('Texto 1')
        self.texto2.color = self.GetColorSafe('Texto 2')         
        self.color_text.color = self.GetColorSafe('Texto')
        self.color_box.bgcolor = self.GetColorSafe('Container')
        self.color_box2.bgcolor = self.GetColorSafe('Fundo')
        self.gradiente.colors = [self.color_box2.bgcolor, self.GetColorSafe('Gradiente')] if __name__ == '__main__' else ['black', 'black']
        self.sombras.color = self.GetColorSafe('Sombras')
        self.bordas = ft.border.all(1, self.GetColorSafe('Bordas'))
        self.botao.bgcolor = self.GetColorSafe('Botao')

        self.color_scheme.primary = self.GetColorSafe("primary")
        self.color_scheme.on_primary = self.GetColorSafe("on_primary")
        self.color_scheme.on_secondary_container = self.GetColorSafe("on_secondary_container")
        self.color_scheme.outline = self.GetColorSafe("outline")
        self.color_scheme.shadow = self.GetColorSafe("shadow")
        self.color_scheme.on_surface_variant = self.GetColorSafe("on_surface_variant")
        self.color_scheme.surface_variant = self.GetColorSafe("surface_variant")
        self.color_scheme.primary_container = self.GetColorSafe("primary_container")
        self.color_scheme.on_surface = self.GetColorSafe("on_surface")
        self.color_scheme.surface = self.color_box2.bgcolor
        self.text_theme.color = self.GetColorSafe("Texto")


        self.ativar_sombras.value = bool(self.GetColorSafe("Ativar Sombras"))
        self.ativar_gradiente.value = bool(self.GetColorSafe("Ativar Gradiente"))
        self.ativar_bordas.value = bool(self.GetColorSafe("Ativar Bordas"))

        self.page.theme = ft.Theme(

            color_scheme=self.color_scheme,
            text_theme = ft.TextTheme(
                body_large = ft.TextStyle(),
                body_medium=self.text_theme,  # Cor do texto padrão
                body_small=ft.TextStyle(),
                title_medium=ft.TextStyle(),

            ),
            scrollbar_theme=ft.ScrollbarTheme(
                thickness = 10,
                cross_axis_margin = -15,
                min_thumb_length = 20,
                track_color = 'grey500',
                thumb_color = 'grey900',
            ),
            elevated_button_theme = ft.ElevatedButtonTheme(
                # bgcolor = self.botao.bgcolor,
                bgcolor = 'green',
            )
        )
        self.dic = {
            "Container": self.color_box.bgcolor,
            "Fundo": self.color_box2.bgcolor,
            "Texto": self.color_text.color,
            "Título": self.titulo.color,
            "Texto 1": self.texto1.color,
            "Texto 2": self.texto2.color,
            "Bordas": self.sombras.color,
            "Sombras": self.sombras.color,
            "Gradiente": self.gradiente.colors,
            "Botão":self.botao.bgcolor,
            "primary":  self.color_scheme.primary,
            "on_primary":  self.color_scheme.on_primary,
            "on_secondary_container":  self.color_scheme.on_secondary_container,
            "outline":  self.color_scheme.outline,
            "shadow":  self.color_scheme.shadow,
            "on_surface_variant":  self.color_scheme.on_surface_variant,
            "surface_variant":  self.color_scheme.surface_variant,
            "primary_container":  self.color_scheme.primary_container,
            "on_surface":  self.color_scheme.on_surface,
            "surface":  self.color_scheme.surface,
        }

        saida = Saida(self.page)
        self.pprint = saida.pprint 
        self.page.horizontal_alignment = 'center'
        self.page.update()

    def CarregarTema(self, e):
        tema = self.tema_escolhido.value
        if tema:
            self.dic = self.arquiv[tema].copy()
            self.titulo.color = self.dic.get('Título')
            self.texto1.color = self.dic.get('Texto 1')
            self.texto2.color = self.dic.get('Texto 2')         
            self.color_text.color = self.dic.get('Texto')
            self.color_box.bgcolor = self.dic.get('Container')
            self.color_box2.bgcolor = self.dic.get('Fundo')
            self.botao.bgcolor = self.dic.get('Botão')

            if isinstance(self.dic.get('Gradiente'), list):
                self.dic['Gradiente'] = self.dic.get('Gradiente')[1]
            if not self.dic.get('Fundo'):
                self.color_box2.bgcolor = 'black'
            if not self.dic.get('Gradiente'):                
                self.gradiente.colors = [self.dic.get('Fundo'),'black']
            else:
                self.gradiente.colors = [self.dic.get('Fundo'), self.dic.get('Gradiente')]

            self.sombras.color = self.dic.get('Sombras')
            self.bordas = ft.border.all(1, self.dic.get('Bordas'))
            self.botao.bgcolor = self.dic.get('Botão')
        

            self.ativar_bordas.value = self.dic.get("Ativar Bordas")
            if self.dic.get("Ativar Bordas"):
                self.color_box.border = self.bordas
            else:
                self.color_box.border = None

            self.ativar_sombras.value = self.dic.get("Ativar Sombras")
            if self.dic.get("Ativar Sombras"):
                self.color_box.shadow = self.sombras
            else:
                self.color_box.shadow = None

            self.ativar_gradiente.value = self.dic.get("Ativar Gradiente")
            if self.color_box2.bgcolor == None:
                self.color_box2.bgcolor = 'black'
            if self.dic.get("Ativar Gradiente"):
                self.gradiente.colors[0] = self.color_box2.bgcolor
                setattr(self.color_box2, 'gradient', self.gradiente)
            else:
                setattr(self.color_box2, 'gradient', None)

            if not self.page.theme:
                self.page.theme = ft.Theme(
                    color_scheme=self.color_scheme,
                    text_theme = ft.TextTheme(
                        body_medium=self.text_theme  # Cor do texto padrão
                    ),
                    scrollbar_theme=ft.ScrollbarTheme(
                        thickness = 10,
                        cross_axis_margin = -15,
                        min_thumb_length = 20,
                        track_color = 'grey500',
                        thumb_color = 'grey900',
                    ),
                    elevated_button_theme = ft.ElevatedButtonTheme(
                        bgcolor = self.dic.get('Botão'),
                    )
                )

            self.color_scheme.primary = self.dic.get("primary")
            self.color_scheme.on_primary = self.dic.get("on_primary")
            self.color_scheme.on_secondary_container = self.dic.get("on_secondary_container")
            self.color_scheme.outline = self.dic.get("outline")
            self.color_scheme.shadow = self.dic.get("shadow")
            self.color_scheme.on_surface_variant = self.dic.get("on_surface_variant")
            self.color_scheme.surface_variant = self.dic.get("surface_variant")
            self.color_scheme.primary_container = self.dic.get("primary_container")
            self.color_scheme.on_surface = self.dic.get("on_surface")
            self.color_scheme.surface = self.dic.get("surface")
            self.text_theme.color = self.dic.get("Texto")

            self.update()
            self.page.update()

    def GetArquivo(self, caminho = None):        
        self.nome_temas = path.join(path.dirname(path.abspath(__file__)), 'Temas.plk')
        caminho = caminho if caminho else self.nome_temas
        self.arquiv = self.LerPickle(caminho) or  {  "black": {
                "Container": "#226076",
                "Fundo": "#1C1E1F",
                "Texto":" #8CC34B",
                "Título": "#2DA860",
                "Texto 1": "#9CA678",
                "Texto 2": "#D9E1E4",
                "Bordas": "#1B232D",
                "Sombras": "#1B232D",
                "Gradiente": "#166A7A",
                "Botão":"#352D4C",
                "primary":  "#CAD0E8",
                "on_primary":  None,
                "on_secondary_container":  None,
                "outline":  None,
                "shadow":  None,
                "on_surface_variant":  None,
                "surface_variant":  None,
                "primary_container":  None,
                "on_surface":  None,
                "surface":  None,
                "secondary": None,
                "error":None,
                "scrim": None,
                "tertiary": None
                
            }
        }
        

    def SalvarPickle(self,  var, nome):
        try:
            if nome[-4:] != '.plk':
                nome += '.plk'
            with open(nome, 'wb') as arquivo:
                dump(var, arquivo)
           
        except PermissionError:
            self.pprint("Permissão negada. Execute o programa como administrador.")

    def LerPickle(self, nome):
        if path.isfile(nome):
            with open(nome, 'rb') as arquivo:
                return load(arquivo)
        else:
            return None   

              

class ConfirmarSaidaeResize:
    def __init__(self,page, funcao = None, exibir = True, width_min = None, height_min = None, onlyresize = False):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.width_min = width_min
        self.height_min = height_min
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.window.on_event = self.window_event
        self.onlyresize = onlyresize
        if not onlyresize:
            self.page.window.prevent_close = True 

        self.page.on_resized = self.page_resize
        # self.page.window.on_event = self.page_resize
        self.nome = f'{self.page.title}_tamanho'
        self.exibir = exibir
        if self.exibir:
            self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
            self.page.overlay.append(self.pw) 
        self.Ler_dados() 


    async def window_event(self, e):
        if e.data == 'resized' or e.data == 'moved':
            await self.page_resize(e)
        if e.data == "close" and not self.onlyresize:
            self.page.overlay.append(self.confirm_dialog)
            
            self.confirm_dialog.open = True
            self.page.update()

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window.destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()



    async def page_resize(self, e):
        if self.exibir:
            self.pw.value = f'{self.page.window.width}*{self.page.window.height} px'
            self.pw.update()
        valores = [self.page.window.width,self.page.window.height,self.page.window.top,self.page.window.left]
        if self.height_min:
            if valores[1]< self.height_min:
                valores[1] = self.height_min
        if self.width_min:
            if valores[0]< self.width_min:
                valores[0] = self.width_min      
        if valores[2] <0:
              valores[2] = 0   
        if valores[3] <0:
              valores[3] = 0                
        # with open('assets/tamanho.txt', 'w') as arq:
        #     arq.write(f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')
        await self.page.client_storage.set_async(self.nome, f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')
        

  

    def Ler_dados(self):
        try:
            # with open('assets/tamanho.txt', 'r') as arq:
            #     po = arq.readline()

            po = self.page.client_storage.get(self.nome)

            p1 = po.split(',')
            p = [int(float(i)) for i in p1]
            po = p[:4] 

            if self.width_min:
                if po[0]< self.width_min:
                    po[0] = self.width_min  
            if self.height_min:
                if po[1]< self.height_min:
                    po[1] = self.height_min 
            if po[2] <0:
                po[2] = 0   
            if po[3] <0:
                po[3] = 0                                   

            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = po
            # print('acerto')
        except:
            # print('erro!')
            # with open('assets/tamanho.txt', 'w') as arq:
            #     arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')
            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = self.width_min,self.height_min,0,0


class Saida:
    def __init__(self,  page = None):
        self.page = page
        self.snac = ft.SnackBar(
            content = ft.Text('', selectable=True, color=ft.Colors.WHITE),
            open=False,

            elevation=2,
            duration=6000,
            show_close_icon=True,  
            close_icon_color  = 'white',                 
            bgcolor=ft.Colors.GREY_900,
            behavior=ft.SnackBarBehavior.FLOATING,
            dismiss_direction=ft.DismissDirection.END_TO_START,
            shape = ft.RoundedRectangleBorder(12)                    
        )
        self.page.overlay.append(self.snac)
 
    
    def pprint(self, *texto):
        self.snac.open = True
        for i in list(texto):
            self.snac.content.value = f'{i}'
            self.page.open(
                self.snac
            )            
        try:
            self.page.update()
        except:
            pass

def main(page):
    page.title = "Seletor de Cores"
    page.window.width = 700
    page.window.height = 300
    page.horizontal_alignment = 'center'
    ConfirmarSaidaeResize(page = page, exibir=False, onlyresize=True)
    page.theme = ft.Theme(
        elevated_button_theme = ft.ElevatedButtonTheme(
            bgcolor   = None,
            icon_color  = None,
            shadow_color  = None,
            text_style = ft.TextStyle(color  = None),
        ),
        checkbox_theme = ft.CheckboxTheme(
            check_color = None,
            fill_color  = None,
        )
    )

    page.add(
        SelectorColor()
    )
def Iniciar():
    ft.app(target=main)
if __name__ == "__main__":  
    ft.app(target=main)
