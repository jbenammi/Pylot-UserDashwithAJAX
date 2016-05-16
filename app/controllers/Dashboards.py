from system.core.controller import *

class Dashboards(Controller):
    def __init__(self, action):
        super(Dashboards, self).__init__(action)

        self.load_model('Dashboard')
        self.db = self._app.db

    def index(self):
         return self.load_view('index.html')

    def welcome(self):
        if 'logged_info' not in session:
            return self.load_view('/partials/welcome.html')
        else:
            return redirect('/view_dash')

    def login_nav(self):
        if 'logged_info' not in session:
            return self.load_view('/partials/navlinks_login.html')
        else:
            return redirect('/loggedin_nav') 

    def view_register(self, errors=None):
        if errors != None:
            flash(errors)
            return self.load_view('/partials/register.html')
        else:
            return self.load_view('/partials/register.html')

    def view_login(self, errors=None):
        if errors != None:
            flash(errors)
        return self.load_view('/partials/login.html')

    def view_dashboard(self):
        user_info = self.models['Dashboard'].get_all_users()
        if session['logged_info']['access'] == 1:
            return self.load_view('/partials/admin_dash.html', users = user_info)
        elif session['logged_info']['access'] == 0:
            return self.load_view('/partials/user_dash.html', users = user_info)


    def loggedin_nav(self):
        if session['logged_info']['access'] == 1:
            return self.load_view('/partials/navlinks_admin.html')
        return self.load_view('/partials/navlinks_user.html')        
    
    def register(self):
        reg_result = self.models['Dashboard'].register_user(request.form)
        if reg_result == 'registered':
            session['registered'] = 'Thank you for Registering. Please Log in'
            return redirect('/v_login')
        else:
            return self.view_register(reg_result)

    def reg_new_user(self):
        reg_result = self.models['Dashboard'].register_user(request.form)
        if reg_result == 'registered':
            return redirect('/view_dash')
        else:
            return self.new_user(reg_result)

    def new_user(self, errors = None):
        if errors != None:
            flash(errors)
            return self.load_view('/partials/new_user.html')
        else:
            return self.load_view('/partials/new_user.html')

    def view_admin_edit(self, id):
        user_info = self.models['Dashboard'].get_user(id)
        return self.load_view('/partials/edit_user.html', user = user_info[0])

    def view_profile(self, id):
        user_info = self.models['Dashboard'].get_user(id)
        return self.load_view('/partials/profile.html', user = user_info[0])

    def edit_user_info(self):
        user = self.models['Dashboard'].update_user_info(request.form)
        return self.view_profile(user)

    def admin_edit_user_info(self):
        user = self.models['Dashboard'].admin_update_user_info(request.form)
        return self.view_dashboard()

    def edit_user_desc(self):
        user = self.models['Dashboard'].update_user_description(request.form)
        return self.view_profile(user)        

    def edit_user_pass(self):
        user = self.models['Dashboard'].update_user_password(request.form)
        if 'id' in user:
            flash({'updated': "Password Updated"})
            return self.view_profile(user['id'])
        else:
            flash(user)
            return self.view_profile(user['user_id'])

    def view_remove_user(self, id):
        print id
        print "*" * 50
        user = self.models['Dashboard'].get_user(id)
        return self.load_view('/partials/remove_user.html', user = user[0])

    def delete_user(self, id):
        self.models['Dashboard'].remove_user(id)
        return redirect('/view_dash')       

    def admin_edit_user_pass(self):
        user = self.models['Dashboard'].update_user_password(request.form)
        if 'id' in user:
            flash({'updated': "Password Updated"})
            return self.view_admin_edit(user['id'])
        else:
            flash(user)
            return self.view_admin_edit(user['user_id'])

    def view_wall(self, id):
        wall_info = self.models['Dashboard'].get_user(id)
        messages = self.models['Dashboard'].get_messages(id)
        comments = self.models['Dashboard'].get_comments(id)
        return self.load_view('/partials/user_wall.html', messages = messages, comments = comments, wall_info = wall_info[0])

    def add_messages(self):
        wall_id = self.models['Dashboard'].add_message(request.form)
        return self.view_wall(wall_id)

    def add_comments(self, id):
        wall_id = self.models['Dashboard'].add_comment(request.form, id)
        return self.view_wall(wall_id)

    def login(self):
        if 'registered' in session:
            del session['registered']
        log_result = self.models['Dashboard'].login_user(request.form)
        if 'logged_info' in log_result:
            session['logged_info'] = log_result['logged_info']
            return self.view_dashboard()
        else:
            return self.view_login(log_result)

    def logout(self):
        print session
        session.clear()
        print session
        return redirect('/welcome')