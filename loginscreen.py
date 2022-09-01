from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager,FadeTransition
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
Window.size=(350,540)
Window.keyboard_anim_args={'d':.2,'t':'in_out_expo'}
Window.softinput_mode='below_target'
Builder.load_file('loginscreen.kv')
Builder.load_file('chatscreen.kv')
Builder.load_file('contentscreen.kv')
Builder.load_file('mainscreen.kv')

class WindowManager(ScreenManager):
	pass

class RegisterContent(MDBoxLayout):

	def register(self):
		import json
		with open('number.json','r') as f:
			k=json.load(f)
		for i in k['Users']:
			if k['Users'][i]['email']==self.ids.reg_email.text:
				print('User email already exist')
				break

		else:
			with open('number.json','r+') as f:
				k=json.load(f)
				l=len(k['Users'])
				user_id='user_'+str(l)
				details={
			    	f"{user_id}":{
					'username':self.ids.reg_user.text,
					'password':self.ids.reg_password.text,
					'email':self.ids.reg_email.text
					}
				}
				k['Users'].update(details)
				f.seek(0)
				json.dump(k,f,indent=4)
				print(self.ids.reg_user.text)

class ForgotContent(MDBoxLayout):
	match=1
	def checking(self):
		import json
		with open('number.json','r+') as f:
			global myuser
			global myemail
			global ID
			k=json.load(f)
		for i in k['Users']:
			if k['Users'][i]['username']==self.ids.check_user.text and \
				k['Users'][i]['email']==self.ids.check_email.text:
				#print('User available, can recover password now')
				myuser=self.ids.check_user.text
				myemail=self.ids.check_email.text
				ID=i
				self.match=2
				break
		else:
			self.match=1
			print('User does not exist')



class GetNewContent(MDBoxLayout):
	def updating(self):
		import json
		with open('number.json','r+') as f:
			k=json.load(f)

			details={
			    	f"{ID}":{
					'username':myuser,
					'password':self.ids.new_passwd.text,
					'email':myemail
					}
				}
			k['Users'].update(details)
			f.seek(0)
			json.dump(k,f,indent=4)

class Screen1(MDScreen):
	def superuser(self):
		pass


	def regpopups(self):
		from kivy.uix.popup import Popup						
		content=RegisterContent(md_bg_color=(1,1,1,1))
		self.popup = Popup(title='Registration',title_size=dp(25),title_align='center',
			content=content,auto_dismiss=True,separator_height=dp(4),
			size_hint=(.95, .95))
		self.popup.open()
		
	def dismisser(self):
		self.popup.dismiss()
		

	def forgpopups(self):
		
		from kivy.uix.popup import Popup						
		content=ForgotContent(md_bg_color=(1,1,1,1))
		self.popup = Popup(title='Password Recovery',title_size=dp(25),title_align='center',
			content=content,auto_dismiss=True,separator_height=dp(4),
			size_hint=(.95, .75))

		self.popup.open()

	def getnewpopups(self):
		from kivy.uix.popup import Popup						
		content=GetNewContent(md_bg_color=(1,1,1,1))
		self.popup = Popup(title='New Password',title_size=dp(25),title_align='center',
			content=content,auto_dismiss=True,separator_height=dp(4),
			size_hint=(.95, .75))
		self.popup.open()

class MyApp(MDApp):
	def build(self):
		self.theme_cls.primary_palette='Teal'
		#self.wm = WindowManager(transition=FadeTransition())
		screens = [Screen1()]
		#for screen in screens:
			#self.wm.add_widget(screen)
		return Screen1()

	def on_start(self):
		import json
		try:
			with open('remember.json','r') as f:
				k=json.load(f)
				self.root.ids.username.text=k['superuser']['username']
				self.root.ids.password.text=k['superuser']['password']

		except:
			pass



	def loginfun(self):
		import json
		f = open('number.json','r')
		k=json.load(f)
		f.close()
		for i in k['Users']:
			#print(i)
			if k['Users'][i]['username']==self.root.ids.username.text and \
					k['Users'][i]['password']==self.root.ids.password.text:
				print('Access allowed')
				
				if self.root.ids.check.active==True:
					detail={"superuser": {"username": self.root.ids.username.text,\
						"password": self.root.ids.password.text}}
					with open('remember.json','w') as f:
						json.dump(detail,f,indent=4)
					print('Details saved for future')
				self.root.ids.username.text=''
				self.root.ids.password.text=''
				break

									
		else:
			print('Wrong entries')
			#self.root.ids.username.text=''
			#self.root.ids.password.text=''

	def change_screen(self, screen):
		'''Change screen using the window manager.'''
		self.wm.current = screen
LabelBase.register(name='Roboto',fn_regular='Jefferies.otf')

if __name__ == '__main__':
	MyApp().run()