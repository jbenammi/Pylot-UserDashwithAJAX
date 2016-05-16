from system.core.router import routes

routes['default_controller'] = 'Dashboards'
routes['GET']['/welcome'] = 'Dashboards#welcome'
routes['GET']['/v_register'] = 'Dashboards#view_register'
routes['GET']['/v_login'] = 'Dashboards#view_login'
routes['GET']['/login_nav'] = 'Dashboards#login_nav'
routes['POST']['/register'] = 'Dashboards#register'
routes['POST']['/login'] = 'Dashboards#login'
routes['GET']['/loggedin_nav'] = 'Dashboards#loggedin_nav'
routes['GET']['/view_dash'] = 'Dashboards#view_dashboard'
routes['GET']['/logout'] = 'Dashboards#logout'
routes['GET']['/view_profile/<id>'] = 'Dashboards#view_profile'
routes['POST']['/edit_user_info'] = 'Dashboards#edit_user_info'
routes['POST']['/edit_description'] = 'Dashboards#edit_user_desc'
routes['POST']['/edit_user_password'] = 'Dashboards#edit_user_pass'
routes['GET']['/new_user'] = 'Dashboards#new_user'
routes['POST']['/reg_new_user'] = 'Dashboards#reg_new_user'
routes['GET']['/v_admin_edit/<id>'] = 'Dashboards#view_admin_edit'
routes['POST']['/admin_edit_user_info'] = 'Dashboards#admin_edit_user_info'
routes['POST']['/admin_edit_user_password'] = 'Dashboards#admin_edit_user_pass'
routes['GET']['/v_remove/<id>'] = 'Dashboards#view_remove_user'
routes['GET']['/delete_user/<id>'] = 'Dashboards#delete_user'
routes['GET']['/messages/<id>'] = 'Dashboards#view_wall'
routes['POST']['/add_message'] = 'Dashboards#add_messages'
routes['POST']['/add_comment/<id>'] = 'Dashboards#add_comments'