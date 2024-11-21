from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
import re
from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.uix.spinner import Spinner
from kivymd.uix.boxlayout import BoxLayout
import requests
from kivy.uix.scrollview import ScrollView
from threading import Thread
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import os
import json
from kivy.core.window import Window
from kivy.uix.label import Label
from datetime import datetime

import asyncpg
import asyncio

Window.clearcolor = (1, 1, 1, 1)

class BancoDeDados:
    async def registrar_chamado_banco(self, chamado, database_url):
        try:
            async with asyncpg.create_pool(dsn=database_url, ssl="require") as pool:
                async with pool.acquire() as connection:
                    if isinstance(chamado, list):  # Se for uma lista de chamados
                        for c in chamado:
                            # Converte a data para datetime
                            data_hora = datetime.strptime(c['data_hora'], '%d/%m/%Y %H:%M:%S')

                            # Certifique-se de que todos os valores estão no formato correto
                            c['chamado'] = str(c['chamado'])  # Convertendo para string, se necessário

                            # Verificar se o chamado já existe
                            result = await connection.fetchrow(
                                "SELECT * FROM chamados WHERE chamado = $1",
                                c['chamado']  # Garantindo que é string
                            )

                            if result:
                                print(f"Chamado {c['chamado']} já existe no banco de dados.")
                            else:
                                # Inserir o novo chamado
                                insert_query = '''
                                INSERT INTO chamados (chamado, nome, matricula, telefone, data_hora, problema, descricao_problema, placa, prefixo, status)
                                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);
                                '''
                                await connection.execute(insert_query,
                                    c['chamado'],  # Garantido como string
                                    c['nome'],  # Garantido como string
                                    c['matricula'],  # Garantido como string
                                    c['telefone'],  # Garantido como string
                                    data_hora,  # datetime
                                    c['problema'],  # Garantido como string
                                    c['descricao_problema'],  # Garantido como string
                                    c['placa'],  # Garantido como string
                                    c['prefixo'],  # Garantido como string
                                    c['status']  # Garantido como string
                                )
                                print(f"Chamado {c['chamado']} registrado com sucesso.")
                    else:  # Caso seja um único chamado
                        # Converte a data para datetime
                        data_hora = datetime.strptime(chamado['data_hora'], '%d/%m/%Y %H:%M:%S')

                        # Certifique-se de que todos os valores estão no formato correto
                        chamado['chamado'] = str(chamado['chamado'])  # Convertendo para string, se necessário

                        # Verificar se o chamado já existe
                        result = await connection.fetchrow(
                            "SELECT * FROM chamados WHERE chamado = $1",
                            chamado['chamado']  # Garantindo que é string
                        )

                        if result:
                            print(f"Chamado {chamado['chamado']} já existe no banco de dados.")
                        else:
                            # Inserir o novo chamado
                            insert_query = '''
                            INSERT INTO chamados (chamado, nome, matricula, telefone, data_hora, problema, descricao_problema, placa, prefixo, status)
                            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);
                            '''
                            await connection.execute(insert_query,
                                chamado['chamado'],  # Garantido como string
                                chamado['nome'],  # Garantido como string
                                chamado['matricula'],  # Garantido como string
                                chamado['telefone'],  # Garantido como string
                                data_hora,  # datetime
                                chamado['problema'],  # Garantido como string
                                chamado['descricao_problema'],  # Garantido como string
                                chamado['placa'],  # Garantido como string
                                chamado['prefixo'],  # Garantido como string
                                chamado['status']  # Garantido como string
                            )
                            print(f"Chamado {chamado['chamado']} registrado com sucesso.")
        except Exception as e:
            print(f"Erro ao registrar o chamado: {e}")

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal" 
        self.theme_cls.theme_style = "Light" 
        
        # Gerenciador de telas
        screen_manager = ScreenManager()

        # TELAS
        screen_manager.add_widget(self.TelaInicial(name="inicial"))
        screen_manager.add_widget(self.TelaInformacoes(name="informacoes"))
        screen_manager.add_widget(self.Dicas(name="dicas"))
        screen_manager.add_widget(self.MeusChamados(name="chamados"))
        screen_manager.add_widget(self.TelaContato(name="contato"))

        return screen_manager
 
    class TelaInicial(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # Imagem na tela inicial
            self.add_widget(Image(source="SOS.png", size_hint=(None, None), size=(300, 200), pos_hint={"center_x": 0.5, "center_y": 0.8}, allow_stretch=True))

            # Campos de texto
            self.matricula_input = MDTextField(
                icon_left="account",
                hint_text="Matrícula",
                text="",
                pos_hint={"center_x": 0.5, "center_y": 0.65},
                size_hint=(0.8, None),
                height=40
            )
            self.add_widget(self.matricula_input)

            self.nome_input = MDTextField(
                icon_left="account-box",
                hint_text="Nome Completo",
                text="",
                pos_hint={"center_x": 0.5, "center_y": 0.55},
                size_hint=(0.8, None),
                height=40
            )
            self.add_widget(self.nome_input)

            self.telefone_input = MDTextField(
                icon_left="phone",
                hint_text="Contato com DDD",
                text="",
                pos_hint={"center_x": 0.5, "center_y": 0.45},
                size_hint=(0.8, None),
                height=40
            )
            self.add_widget(self.telefone_input)

            # Botão de prosseguir
            botao_proseguir = MDFlatButton(
                text="Prosseguir",
                md_bg_color=(0, 128 / 255, 128 / 255, 1),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.35},
                size_hint=(0.8, None),
                height=50
            )
            botao_proseguir.bind(on_press=self.proseguir)
            self.add_widget(botao_proseguir)

        def proseguir(self, instance):
            matricula = self.matricula_input.text
            nome = self.nome_input.text
            telefone = self.telefone_input.text

            # Validações
            if not matricula or not nome or not telefone:
                self.show_dialog("ERRO", "Todos os campos devem ser preenchidos.")
                return

            if not matricula.isdigit():
                self.show_dialog("ERRO", "A matrícula deve conter apenas números.")
                return

            if not re.match("^[a-zA-Z ]+$", nome):
                self.show_dialog("ERRO", "O nome deve conter apenas letras.")
                return False

            if not re.match(r'^\d{11}$', telefone):
                self.show_dialog("ERRO", "O telefone deve ter 11 dígitos.")
                return

            # Passando valores para a próxima tela
            informacoes_screen = self.manager.get_screen('informacoes')
            informacoes_screen.update_info(nome, matricula, telefone)

            # Avança para a próxima tela
            self.manager.current = "informacoes"

        def show_dialog(self, title, message):
            self.dialog = MDDialog(
                title=title,
                text=message,
                size_hint=(0.8, None),
                height="200dp",
                buttons=[MDFlatButton(text="OK", size_hint=(0.8, None), height="50dp", on_release=self.close_dialog)]
            )
            self.dialog.open()

        def close_dialog(self, instance):
            self.dialog.dismiss()

        def limpar_campos(self):
            self.matricula_input.text = ""
            self.nome_input.text = ""
            self.telefone_input.text = ""

    class TelaInformacoes(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            scroll_view = ScrollView(size_hint=(1, None), height=Window.height, pos_hint={"top": 1})
            self.scroll_content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10) 
            self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))

            self.voltar_button = MDIconButton(
                icon="arrow-left",
                pos_hint={"top": 1},
                size_hint=(None, None),
                size=("40dp", "40dp"),
                on_release=self.voltar
            )
            self.scroll_content.add_widget(self.voltar_button)

            self.nome_input = MDRectangleFlatIconButton(
                icon="account",
                icon_color=(0, 0, 0, 1),
                text_color=(0, 0, 0, 1),
                md_bg_color=(1, 1, 1, 0),
                size_hint=(0.8, None),
                height=40,
                pos_hint={"center_x": 0.5},
                disabled=False,
                on_release=self.abrir_chamados
            )
            self.scroll_content.add_widget(self.nome_input)

            self.placa_input = MDTextField(
                hint_text="Placa do Veículo",
                size_hint=(0.8, None),
                height=40,
                pos_hint={"center_x": 0.5}
            )

            self.prefixo_input = MDTextField(
                hint_text="Prefixo",
                size_hint=(0.8, None),
                height=40,
                pos_hint={"center_x": 0.5}
            )

            self.problema_spinner = Spinner(
                text="Selecione o Problema",
                values=sorted([  # Ordena os valores em ordem alfabética
                    "Encerrar Atendimento",
                    "Finalizar BDV",
                    "Quilometragem Divergente",
                    "Tela de Carregamento",
                    "Alterar Escala",
                    "Alterar Prefixo",
                    "Alterar Placa do Veículo",
                    "Alterar Base",
                    "Usuário Bloqueado",
                    "Outros"
                ]),
                size_hint=(0.8, None),
                height=50,
                pos_hint={"center_x": 0.5},
            )
            self.problema_spinner.bind(text=self.atualizar_interface_spinner)

            self.observacoes_input = MDTextField(
                hint_text="Descrição do Problema",
                size_hint=(0.8, None),
                height=40,
                pos_hint={"center_x": 0.5},
                disabled=False
            )

            self.botao_proseguir = MDRaisedButton(
                text="Prosseguir",
                md_bg_color=(0, 128 / 255, 128 / 255, 1),
                text_color=(1, 1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.2},
                size_hint=(0.8, None),
                height=50,
                on_release=self.executar_funcao
            )
            self.botao_proseguir.bind(on_press=self.executar_funcao)

            self.add_widget(scroll_view)
            scroll_view.add_widget(self.scroll_content) 
            self.scroll_content.add_widget(self.placa_input)
            self.scroll_content.add_widget(self.prefixo_input)
            self.scroll_content.add_widget(self.problema_spinner)
            self.scroll_content.add_widget(self.observacoes_input)
            self.scroll_content.add_widget(self.botao_proseguir)

        def atualizar_interface_spinner(self, spinner, text):
            for widget in list(self.scroll_content.children):
                if widget not in [self.voltar_button, self.nome_input, self.placa_input, self.prefixo_input,self.problema_spinner]:
                    self.scroll_content.remove_widget(widget)

            if text == "Quilometragem Divergente":
                self.km_errado = MDTextField(
                    hint_text="Quilometragem Registrada Incorretamente",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                )
                self.km_certo = MDTextField(
                    hint_text="Quilometragem Correta",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                )
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.km_errado)
                self.scroll_content.add_widget(self.km_certo)
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)
                self.botao_proseguir.bind(on_press=self.executar_funcao)

            elif text == "Encerrar Atendimento" or text == "Finalizar BDV":
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)

            elif text == "Alterar Escala":
                self.escala_input = MDTextField(
                    hint_text="Escala Correta",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.escala_input)
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)
                self.botao_proseguir.bind(on_press=self.executar_funcao)

            elif text == "Alterar Placa do Veículo":
                self.placacorreta_input = MDTextField(
                    hint_text="Placa Correta",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.placacorreta_input)
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)
                self.botao_proseguir.bind(on_press=self.executar_funcao)

            elif text == "Alterar Prefixo":
                self.prefixocorreto_input = MDTextField(
                    hint_text="Prefixo Correto",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.prefixocorreto_input)
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)
                self.botao_proseguir.bind(on_press=self.executar_funcao)

            elif text == "Alterar Base":
                self.base_input = MDTextField(
                    hint_text="Base Correta",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.base_input)
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)
                self.botao_proseguir.bind(on_press=self.executar_funcao)

            elif text == "Usuário Bloqueado":
                self.matricula_input = MDTextField(
                    hint_text="Matrícula do Usuário",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.matricula_input)
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)
                self.botao_proseguir.bind(on_press=self.executar_funcao)

            elif text == "Tela de Carregamento":
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)
                self.botao_proseguir.bind(on_press=self.executar_funcao)

            elif text == "Outros":
                self.observacoes_input = MDTextField(
                    hint_text="Descrição do Problema",
                    size_hint=(0.8, None),
                    height=40,
                    pos_hint={"center_x": 0.5},
                    disabled=False
                )
                self.scroll_content.add_widget(self.observacoes_input)
                self.scroll_content.add_widget(self.botao_proseguir)
                self.botao_proseguir.bind(on_press=self.executar_funcao)

        def update_info(self, nome, matricula, telefone):
            self.nome_input.text = f"{matricula} - {nome}"
            self.matricula = matricula
            self.telefone = telefone
            self.nome = nome

        def voltar(self, instance):
            inicial = self.manager.get_screen("inicial")
            inicial.limpar_campos()
            self.manager.current = "inicial"

        def abrir_chamados(self, instance):
            placa = self.placa_input.text
            matricula = self.matricula
            chamados = self.manager.get_screen('chamados')
            chamados.update_info(matricula,placa)
            self.manager.current = "chamados"

        def exibir_erro(self, mensagem):

            if hasattr(self, 'dialog') and self.dialog:
                self.dialog.dismiss()
                self.dialog = None

            self.dialog = MDDialog(
                title="ERRO",
                text=mensagem,
                size_hint=(0.8, None),
                height="200dp",
                buttons=[MDFlatButton(
                    text="OK", 
                    on_release=self.fechar_dialogo
                )]
            )
            self.dialog.open()

        def executar_funcao(self, instance):
            problema = self.problema_spinner.text
            nome = self.nome
            matricula = self.matricula
            telefone = self.telefone
            placa = self.placa_input.text
            prefixo = self.prefixo_input.text

            if hasattr(self, 'observacoes_input'):
                descricao = self.observacoes_input.text
            else:
                descricao = ""

            if hasattr(self, 'km_certo') and hasattr(self, 'km_errado'):
                km_certo = self.km_certo.text
                km_errado = self.km_errado.text
            else:
                km_certo = ""
                km_errado = ""

            if hasattr(self, 'escala_input'):
                escala = self.escala_input.text
            else:
                escala = ""

            if hasattr(self, 'prefixocorreto_input'):
                prefixocorreto = self.prefixocorreto_input.text
            else:
                prefixocorreto = ""

            if hasattr(self, 'placacorreta_input'):
                placacorreta = self.placacorreta_input.text
            else:
                placacorreta = ""

            if hasattr(self, 'base_input'):
                base = self.base_input.text
            else:
                base = ""

            if len(placa) != 7:
                self.exibir_erro("Verifique a placa do veículo.")
                return
            
            if len(prefixo) < 4:
                self.exibir_erro("Verifique o prefixo.")
                return  

            if problema == "Encerrar Atendimento" or problema == "Finalizar BDV":
                dicas_screen = self.manager.get_screen('dicas')
                dicas_screen.update_info(nome, matricula, telefone, problema, placa, prefixo, descricao, km_certo, km_errado, escala, base)
                self.manager.current = "dicas"

            elif problema == "Quilometragem Divergente":
                if km_errado != "" and km_certo != "":
                    contato_screen = self.manager.get_screen('contato')
                    contato_screen.update_info(nome, matricula, telefone, problema, placa,placacorreta, prefixo, descricao, km_certo, km_errado, escala, base, prefixocorreto)
                    self.manager.current = "contato"
                else:    
                    self.exibir_erro("Preencha todos os campos.")
                    return 

            elif problema == "Tela de Carregamento":
                contato_screen = self.manager.get_screen('contato')
                contato_screen.update_info(nome, matricula, telefone, problema, placa,placacorreta, prefixo, descricao, km_certo, km_errado, escala, base, prefixocorreto)
                self.manager.current = "contato"

            elif problema == "Alterar Escala":
                if escala != "":
                    contato_screen = self.manager.get_screen('contato')
                    contato_screen.update_info(nome, matricula, telefone, problema, placa,placacorreta, prefixo, descricao, km_certo, km_errado, escala, base, prefixocorreto)
                    self.manager.current = "contato"
                else:    
                    self.exibir_erro("Informe a escala correta.")
                    return 

            elif problema == "Alterar Prefixo":
                if prefixocorreto != "":
                    contato_screen = self.manager.get_screen('contato')
                    contato_screen.update_info(nome, matricula, telefone, problema, placa,placacorreta, prefixo, descricao, km_certo, km_errado, escala, base, prefixocorreto)
                    self.manager.current = "contato"
                else:    
                    self.exibir_erro("Informe o prefixo correto.")
                    return 

            elif problema == "Alterar Placa do Veículo":
                if placa != "":
                    contato_screen = self.manager.get_screen('contato')
                    contato_screen.update_info(nome, matricula, telefone, problema, placa,placacorreta, prefixo, descricao, km_certo, km_errado, escala, base, prefixocorreto)
                    self.manager.current = "contato"
                else:    
                    self.exibir_erro("Informe a placa correta.")
                    return 

            elif problema == "Alterar Base":
                if base != "":
                    contato_screen = self.manager.get_screen('contato')
                    contato_screen.update_info(nome, matricula, telefone, problema, placa,placacorreta, prefixo, descricao, km_certo, km_errado, escala, base, prefixocorreto)
                    self.manager.current = "contato"
                else:    
                    self.exibir_erro("Informe a base correta.")
                    return 

            elif problema == "Usuário Bloqueado":
                if self.matricula_input.text != "":
                    contato_screen = self.manager.get_screen('contato')
                    contato_screen.update_info(nome, matricula, telefone, problema, placa,placacorreta, prefixo, descricao, km_certo, km_errado, escala, base, prefixocorreto)
                    self.manager.current = "contato"
                else:    
                    self.exibir_erro("Informe a matrícula do usuário bloqueado.")
                    return

            elif problema == "Outros":
                if descricao != "":
                    contato_screen = self.manager.get_screen('contato')
                    contato_screen.update_info(nome, matricula, telefone, problema, placa,placacorreta, prefixo, descricao, km_certo, km_errado, escala, base, prefixocorreto)
                    self.manager.current = "contato"
                else:    
                    self.exibir_erro("Descreva o problema no campo de observações.")
                    return 

            elif problema == "Selecione o Problema":
                self.exibir_erro("Selecione o motivo do chamado.")

        def fechar_dialogo(self, instance):
            if hasattr(self, 'dialog') and self.dialog:
                self.dialog.dismiss() 
                self.dialog = None

    class Dicas(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)


            self.problema = ""
            self.usuario = ""
            self.matricula = ""
            self.telefone = ""
            self.responsavel = ""
            self.status = ""
            self.placa = ""
            self.prefixo = ""
            self.descricao = ""

            # Tela rolante (Scroll View) para os campos e entradas
            scroll_view = ScrollView(size_hint=(1, None), height=Window.height,pos_hint={"top": 1})
            scroll_content = BoxLayout(orientation='vertical', size_hint_y=None,spacing=10,padding=[20, 0, 20, 0])
            scroll_content.bind(minimum_height=scroll_content.setter('height'))
            
            scroll_content.add_widget(MDIconButton(
                icon="arrow-left",
                pos_hint={"top": 1},
                size_hint=(None, None),
                size=("40dp", "40dp"),
                on_release=self.voltar
            ))

            self.titulo_label = Label(
                text="Título",
                size_hint_y=None,
                height=40,
                halign='center',
                font_size=18,
                color=(0, 0, 0, 1)
            )
            scroll_content.add_widget(self.titulo_label)


            self.instrucoes_input = MDLabel(
                text="Este é o conteúdo do campo de texto transformado em um Label.",
                size_hint_y=None,
                height=440,  # Ajuste o tamanho conforme necessário
                halign="left",
                font_size=14,
                padding=[10, 10],
            )
            scroll_content.add_widget(self.instrucoes_input)

            scroll_view.add_widget(scroll_content)
            self.add_widget(scroll_view)

            # Container para os botões SIM e NÃO
            botoes_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=120,
                spacing=10,
                padding=[10, 10]
            )

            btn_sim = MDFlatButton(
                text="SIM",
                md_bg_color=(0, 128 / 255, 128 / 255, 1),
                theme_text_color="Custom",
                text_color=(1, 1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.2},
                size_hint=(0.8, None),
                height=50,
            )
            btn_sim.bind(on_press=self.resposta_sim)
            botoes_layout.add_widget(btn_sim)

            btn_nao = MDFlatButton(
                text="NÃO",
                md_bg_color=(0, 128 / 255, 128 / 255, 1),
                theme_text_color="Custom",
                text_color=(1, 1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.2},
                size_hint=(0.8, None),
                height=50
            )
            btn_nao.bind(on_press=self.resposta_nao)
            botoes_layout.add_widget(btn_nao)

            # Adicionando os botões ao conteúdo da tela
            scroll_content.add_widget(botoes_layout)

        def update_info(self,nome, matricula, telefone, problema, placa,prefixo, descricao,km_certo,km_errado,escala,base):
            self.titulo_label.text = problema
            self.problema = problema
            self.matricula = matricula
            self.placa = placa
            self.prefixo = prefixo
            self.usuario = nome
            self.telefone = telefone
            self.instrucoes = self.atualizar_texto()
            self.instrucoes_input.text = self.instrucoes
            self.descricao = descricao
            self.km_certo = km_certo
            self.km_errado = km_errado
            self.escala = escala
            self.prefixo = prefixo
            self.base = base

            agora = datetime.now()

            dia_da_semana = agora.weekday()  
            
            hora_atual = agora.hour
            minuto_atual = agora.minute
            horario_valido = (hora_atual > 7 or (hora_atual == 7 and minuto_atual >= 0)) and \
                            (hora_atual < 16 or (hora_atual == 16 and minuto_atual <= 30))

            if 0 <= dia_da_semana <= 4 and horario_valido:
                self.status =  "disponível"
            else:
                self.status =  "indisponível"

        def voltar(self, instance):
            self.manager.current = "informacoes"

        def ver_chamados(self, instance):
            self.manager.current = "chamados"

        def fechar_dialogo_com_erro(self, instance):
            self.dialog.dismiss()

        def verificar_conexao(self):
            try:
                requests.get("https://www.google.com", timeout=5)
                return True
            except requests.ConnectionError:
                return False
            
        def iniciar_thread_assincrona(self, chamado, database_url):
            # Envolva a função assíncrona em um evento asyncio para executá-la em um loop
            def run_async():
                asyncio.run(BancoDeDados().registrar_chamado_banco(chamado, database_url))
            
            # Crie uma thread para executar o evento asyncio
            thread = Thread(target=run_async)
            thread.start()


        def resposta_sim(self, instance):
            
            timestamp = datetime.now().strftime("%d%m%Y%H%M%S")

            numero_chamado = f"CH{timestamp}"

            chamado = {
                "chamado":timestamp,
                "nome": self.usuario,
                "matricula": self.matricula,
                "telefone": self.telefone,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "problema": self.problema,
                "descricao_problema": self.descricao,
                "placa":self.placa,
                "prefixo":self.prefixo,
                "status": "Finalizado"
            }


            self.dialog = MDDialog(
                    title="Chamado Finalizado",
                    text=f"Seu chamado {numero_chamado} foi registrado e encerrado.",
                    size_hint=(0.8, None),
                    height="200dp",
                    buttons=[MDFlatButton(
                        text="OK", 
                        on_release=self.fechar_dialogo_com_erro
                    )]
                )
            self.dialog.open()

            try:

                with open("chamados.json", "r", encoding="utf-8") as file:
                    chamados = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # Se não existir ou estiver vazio, cria a lista de chamados
                chamados = []

            chamados.append(chamado)

            with open("chamados.json", "w", encoding="utf-8") as file:
                json.dump(chamados, file, indent=4, ensure_ascii=False)
            
                chamados_screen = self.manager.get_screen("chamados")
                chamados_screen.chamados_data = chamados
                chamados_screen.atualizar()
                database_url = "postgresql://postgres:nxBbiONUuVaFqDvIpZHQAAhtkaMechpq@junction.proxy.rlwy.net:23366/railway"
                json_file_path = "chamados.json"

                self.iniciar_thread_assincrona(chamado, database_url)
                self.manager.current = "inicial" 

        def resposta_nao(self, instance):
            timestamp = datetime.now().strftime("%d%m%Y%H%M%S")

            numero_chamado = f"CH{timestamp}"

            chamado = {
                "chamado": timestamp,
                "nome": self.usuario,
                "matricula": self.matricula,
                "telefone": self.telefone,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "problema": self.problema,
                "descricao_problema": self.descricao,
                "placa":self.placa,
                "prefixo":self.prefixo,
                "status": "Aberto"
            }

            self.dialog = MDDialog(
                    title="Chamado Aberto",
                    text=f"Seu chamado {numero_chamado} foi registrado. Aguarde retorno do responsável.",
                    size_hint=(0.8, None),
                    height="200dp",
                    buttons=[MDFlatButton(
                        text="OK", 
                        on_release=self.fechar_dialogo_com_erro
                    )]
                )
            self.dialog.open()

            try:

                with open("chamados.json", "r", encoding="utf-8") as file:
                    chamados = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # Se não existir ou estiver vazio, cria a lista de chamados
                chamados = []

            chamados.append(chamado)

            with open("chamados.json", "w", encoding="utf-8") as file:
                json.dump(chamados, file, indent=4, ensure_ascii=False)
            
                chamados_screen = self.manager.get_screen("chamados")
                chamados_screen.chamados_data = chamados
                chamados_screen.atualizar() 

                database_url = "postgresql://postgres:nxBbiONUuVaFqDvIpZHQAAhtkaMechpq@junction.proxy.rlwy.net:23366/railway"
                json_file_path = "chamados.json"

                self.iniciar_thread_assincrona(chamado, database_url)
                self.manager.current = "chamados"

        def atualizar_texto(self):
            problema = self.problema

            print(self.problema)
            if self.problema == "Encerrar Atendimento":
                return "Se o aplicativo do BDV apresenta erro ao encerrar o atendimento, siga as instruções a seguir:\n1 - Insista algumas vezes. Clique em OK, aguarde 2 segundos e tente encerrar novamente.\nSe o erro persistir:\n2 - Anote a quilometragem inicial e final do seu atendimento, e matricula dos passageiros (se houver).\n3 - Selecione o ícone de usuário no canto inferior direito e escolha 'SAIR'\nVocê provavelmente vai receber uma mensagem de confirmação afirmando que o atendimento será perdido. Confirme.\nSe preferir reinicie o celular.\n4 - Faça login novamente.\n5 - Abra o atendimento novamente com a quilometragem inicial que você anotou.\n6 - Escreva no campo de observações seu local de inicio e fim do atendimento e outras informações relevantes.\n7 - Encerre o atendimento com a quilometragem final que você anotou.\n\n\nEssas informações resolveram seu problema?"
            elif problema == "Finalizar BDV":
                return "Se o aplicativo está apresentando erro para finalizar o BDV, siga as instruções a seguir:\n1 - Verifique sua conexão com a internet.\n2 - Verifique se a tela de finalização está completamente carregada e se o número do BDV é diferente de 0. Esse processo de carregamento pode demorar alguns segundos dependendo da sua conexão com a internet.\n3 - Após todas as informações carregadas e o número do BDV gerado, aguarde alguns segundos enquanto confere seus antendimentos registrados, depois confirme a finalização.\nSe mesmo assim ocorrer erro, selecione o ícone de usuário no canto inferior direito, selecione 'SAIR', faça login novamente repita o processo de finalização\n\nIMPORTANTE: É NECESSÁRIO FINALIZAR O BDV.\nSe sair e não voltar para finalizar os próximos usuários não conseguirão utilizar o aplicativo.\n\n\nEssas informações resolveram seu problema?"
                return "Problema não identificado. Consulte o suporte técnico."

    class MeusChamados(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.matricula = None  
            self.placa = None  

            self.chamados_data = self.carregar_chamados()

            scroll_view = ScrollView(size_hint=(1, None), height=Window.height, pos_hint={"top": 1})
            self.scroll_content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
            self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))

            self.voltar_button = MDIconButton(
                icon="arrow-left",
                pos_hint={"top": 1},
                size_hint=(None, None),
                size=("40dp", "40dp"),
                on_release=self.voltar
            )
            self.scroll_content.add_widget(self.voltar_button)

            self.atualizar()  
            self.add_widget(scroll_view)
            scroll_view.add_widget(self.scroll_content)

        def update_info(self, matricula, placa):
            self.matricula = matricula  
            self.placa = placa  
            self.atualizar()  

        def atualizar(self):
            if self.matricula is None or self.placa is None:
                print("Matrícula ou placa não definidas")
                return

            for widget in self.scroll_content.children[:]:
                if isinstance(widget, BoxLayout):
                    self.scroll_content.remove_widget(widget) 

            chamados_filtrados = self.filtrar_chamados(self.chamados_data)
            chamados_filtrados.sort(key=lambda chamado: chamado['data_hora'], reverse=True)

            for chamado in chamados_filtrados:
                self.scroll_content.add_widget(self.criar_card_chamado(chamado))

        def carregar_chamados(self):
            with open('chamados.json', 'r', encoding='utf-8') as file:
                return json.load(file)

        def filtrar_chamados(self, chamados):
            chamados_filtrados = []

            for chamado in chamados:

                if chamado['matricula'] == self.matricula:
                    chamados_filtrados.append(chamado)

                elif chamado['status'] == "Aberto" and chamado['placa'] == self.placa:
                    chamados_filtrados.append(chamado)

            return chamados_filtrados

        def criar_card_chamado(self, chamado):
            # Cria o card do chamado para exibição
            card = MDCard(
                orientation='vertical',
                size_hint=(0.8, None),
                size=("280dp", "120dp"),
                pos_hint={"center_x": 0.5},
                padding=10,
                spacing=12
            )
            
            card.add_widget(MDLabel(text=f"Chamado: {chamado['chamado']}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Solicitante: {chamado['nome']} - {chamado['matricula']}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Contato: {chamado['telefone']}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Prefixo: {chamado['prefixo']} - Placa: {chamado['placa']}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Data: {chamado['data_hora']}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Problema: {chamado['problema']}", theme_text_color="Secondary"))
            if chamado['descricao_problema'] != "":
                card.add_widget(MDLabel(text=f"Descrição: {chamado['descricao_problema']}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Status: {chamado['status']}", theme_text_color="Secondary"))  

            return card

        def voltar(self, instance):
            self.manager.current = "informacoes"

    class TelaContato(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            scroll_view = ScrollView(size_hint=(1, None), height=Window.height, pos_hint={"top": 1})
            self.scroll_content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)  # Make it an instance attribute
            self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))

            # Botão de voltar
            self.voltar_button = MDIconButton(
                icon="arrow-left",
                pos_hint={"top": 1},
                size_hint=(None, None),
                size=("40dp", "40dp"),
                on_release=self.voltar
            )
            self.scroll_content.add_widget(self.voltar_button)

            self.nome_input = MDTextField(
                hint_text="Solicitante",
                pos_hint={"center_x": 0.5, "center_y": 0.55},
                size_hint=(0.8, None),
                height=40,
                disabled=True
            )
            self.scroll_content.add_widget(self.nome_input)

            self.matricula_input = MDTextField(
                hint_text="Matrícula",
                pos_hint={"center_x": 0.5, "center_y": 0.55},
                size_hint=(0.8, None),
                height=40,
                disabled=True
            )
            self.scroll_content.add_widget(self.matricula_input)

            self.telefone_input = MDTextField(
                hint_text="Contato",
                pos_hint={"center_x": 0.5, "center_y": 0.55},
                size_hint=(0.8, None),
                height=40,
                disabled=True
            )
            self.scroll_content.add_widget(self.telefone_input)

            self.placa_input = MDTextField(
                hint_text="Placa do Veículo",
                pos_hint={"center_x": 0.5, "center_y": 0.55},
                size_hint=(0.8, None),
                height=40,
                disabled=True
            )
            self.scroll_content.add_widget(self.placa_input)

            self.prefixo_input = MDTextField(
                hint_text="Prefixo",
                pos_hint={"center_x": 0.5, "center_y": 0.55},
                size_hint=(0.8, None),
                height=40,
                disabled=True
            )
            self.scroll_content.add_widget(self.prefixo_input)

            self.problema_input = MDTextField(
                hint_text="Problema",
                pos_hint={"center_x": 0.5, "center_y": 0.55},
                size_hint=(0.8, None),
                height=40,
                disabled=True
            )
            self.scroll_content.add_widget(self.problema_input)

            self.descricao_input = MDTextField(
                hint_text="Descrição",
                pos_hint={"center_x": 0.5, "center_y": 0.55},
                size_hint=(0.8, None),
                height=40,
                disabled=True
            )
            self.scroll_content.add_widget(self.descricao_input)

            self.abrir_chamado = MDFlatButton(
                text="Abrir Chamado",
                md_bg_color=(0, 128 / 255, 128 / 255, 1),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.35},
                size_hint=(0.8, None),
                height=50
            )
            self.abrir_chamado.bind(on_press=self.confirmar_chamado)
            self.scroll_content.add_widget(self.abrir_chamado)

            self.add_widget(scroll_view)
            scroll_view.add_widget(self.scroll_content)

        def voltar(self, instance):
            self.manager.current = "informacoes"

        def iniciar_thread_assincrona(self, chamado, database_url):
            # Envolva a função assíncrona em um evento asyncio para executá-la em um loop
            def run_async():
                asyncio.run(BancoDeDados().registrar_chamado_banco(chamado, database_url))
            
            # Crie uma thread para executar o evento asyncio
            thread = Thread(target=run_async)
            thread.start()


        def update_info(self, nome, matricula, telefone, problema, placa,placacorreta,prefixo, descricao, km_certo, km_errado, escala, base,prefixocorreto):
             
            self.nome_input.text = nome
            self.matricula_input.text = matricula
            self.telefone_input.text = telefone
            self.problema_input.text = problema
            self.escala = escala
            self.base = base
            self.placa_input.text = placa
            self.prefixo_input.text = prefixo
            self.descricao_input.text = descricao
            self.prefixocorreto = prefixocorreto
            self.placacorreta = placacorreta

            if problema == "Quilometragem Divergente":
                self.descricao_input.text = f"KM Errado: {km_errado}, KM Certo: {km_certo} - {descricao}"
            elif problema == "Alterar Base":
                self.descricao_input.text = f"Base Correta: {base} - {descricao}"
            elif problema == "Alterar Prefixo":
                self.descricao_input.text = f"Prefixo Correto: {prefixocorreto} - {descricao}"
            elif problema == "Alterar Placa do Veículo":
                self.descricao_input.text = f"Placa Correta: {placacorreta} - {descricao}"
            elif problema == "Alterar Escala":
                self.descricao_input.text = f"Escala Correta: {escala} - {descricao}"

        def verificar_conexao(self):
            try:
                requests.get("https://www.google.com", timeout=5)
                return True
            except requests.ConnectionError:
                return False
            

        # Função para atualizar o arquivo JSON
        def atualizar_json(self, chamado, json_file_path):
            try:
                # Carregar os dados atuais do arquivo JSON
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    chamados_data = json.load(f)

                # Adicionar o novo chamado ao JSON
                chamados_data.append(chamado)

                # Salvar novamente o arquivo JSON
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(chamados_data, f, ensure_ascii=False, indent=4)

                print("Arquivo JSON atualizado com o novo chamado.")

            except Exception as e:
                print(f"Erro ao atualizar o arquivo JSON: {e}")

        # Método para confirmar o chamado
        def confirmar_chamado(self, instance):
            timestamp = int(datetime.now().timestamp())
            numero_chamado = f"CH{timestamp}"

            chamado = {
                "chamado": timestamp,
                "nome": self.nome_input.text,
                "matricula": self.matricula_input.text,
                "telefone": self.telefone_input.text,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "problema": self.problema_input.text,
                "descricao_problema": self.descricao_input.text,
                "placa": self.placa_input.text,
                "prefixo": self.prefixo_input.text,
                "status": "Aberto"
            }

            self.salvar_chamado(chamado)

            self.exibir_dialogo_chamado(numero_chamado)

            database_url = "postgresql://postgres:nxBbiONUuVaFqDvIpZHQAAhtkaMechpq@junction.proxy.rlwy.net:23366/railway"
            json_file_path = "chamados.json"

            # Chama a thread para processar o chamado e os dados ausentes no banco
            self.iniciar_thread_assincrona(chamado, database_url)

        def salvar_chamado(self, chamado):
            try:
                with open("chamados.json", "r", encoding="utf-8") as file:
                    chamados = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                chamados = []

            chamados.append(chamado)

            with open("chamados.json", "w", encoding="utf-8") as file:
                json.dump(chamados, file, indent=4, ensure_ascii=False)
            
            chamados_screen = self.manager.get_screen("chamados")
            chamados_screen.chamados_data = chamados
            chamados_screen.atualizar() 

        def exibir_dialogo_chamado(self, numero_chamado):
            if hasattr(self, 'dialog') and self.dialog:
                self.dialog.dismiss()
                self.dialog = None

            self.dialog = MDDialog(
                title="Chamado Registrado",
                text=f"O número do seu chamado é {numero_chamado}.",
                size_hint=(0.8, None),
                height="200dp",
                buttons=[MDFlatButton(
                    text="OK", 
                    on_release=self.fechar_dialogo
                )]
            )
            self.dialog.open()

        def fechar_dialogo(self, instance):
            if hasattr(self, 'dialog') and self.dialog:
                self.dialog.dismiss() 
                self.dialog = None
            self.manager.current = "inicial"

if __name__ == "__main__":
    MyApp().run()
