from system.core.model import Model
import re
EMAILREGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
class Dashboard(Model):
    def __init__(self):
        super(Dashboard, self).__init__()

    def register_user(self, reginfo):
        errors = {}
        if len(reginfo['fname']) < 2:
            errors.update({'fname': 'The first name field must be at least two characters'})
        elif not str.isalpha(str(reginfo['fname'])):
            errors.update({'fname': 'First name cannot have number or symbols'})
        if len(reginfo['lname']) < 2:
            errors.update({'lname': 'The last name field must be at least two characters'})
        elif not str.isalpha(str(reginfo['lname'])):
            errors.update({'lname': 'Last name cannot have numbers or symbols'})
        if not EMAILREGEX.match(reginfo['email']):
            errors.update({'email': 'The E-Mail must be a valid e-mail address'})
        if len(reginfo['password']) < 8:
            errors.update({'password': 'Password must be at least 8 characters'})
        elif not any(char.isdigit() for char in str(reginfo['password'])):
            errors.update({'password': 'Password must contain at least one number'})
        elif not any(char.isupper() for char in str(reginfo['password'])):
            errors.update({'password': 'Password must contain at least one uppercase letter'})
        if reginfo['confirmpass'] != reginfo['password']:
            errors.update({'confirmpass': 'The password confirmation does not match the password'})
        if len(errors) > 0:
            return errors
        else:
            query1 = "SELECT email FROM users WHERE email = :email"
            data1 = {"email": reginfo['email']}
            if not self.db.query_db(query1, data1):
                pw_hash = self.bcrypt.generate_password_hash(reginfo['password'])
                query = "INSERT INTO users(first_name, last_name, email, password, created_on, updated_on) VALUES(:first_name, :last_name, :email, :password, now(), now())"
                info = {
                "first_name": reginfo['fname'],
                "last_name": reginfo['lname'],
                "email": reginfo['email'],
                "password": pw_hash
                }
                self.db.query_db(query, info)
                return "registered"
            else:
                errors.update({'user_registered': 'This E-Mail is already registered'})
                return errors

    def login_user(self, loginfo):
        errors = {}
        if not EMAILREGEX.match(loginfo['email']):
            errors.update({'email2': 'The E-Mail must be a valid e-mail address'})
        if len(loginfo['password']) < 8:
            errors.update({'password2': 'Password must be at least 8 characters'})
        if len(errors) > 0:
            return errors
        else:
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = {'email': loginfo['email']}
            user = self.db.query_db(query, data)
            if user == []:
                errors.update({'notreg': 'E-Mail is not registered.'})
                return errors
            else:
                if self.bcrypt.check_password_hash(user[0]['password'], loginfo['password']):
                    logged_info = {'logged_info':{'id': user[0]['id'], 'first_name': user[0]['first_name'], 'last_name': user[0]['last_name'], 'access': user[0]['access']}}
                    return logged_info
                else:
                    errors.update({'passmatch': 'Incorrect password entered for registered E-Mail.'})
                    return errors

    def get_all_users(self):
        query = "SELECT id as user_id, first_name, last_name, email, access, created_on FROM users"
        return self.db.query_db(query)

    def get_user(self, id):
        query = "SELECT id as user_id, first_name, last_name, email, description, access, created_on FROM users WHERE id = :id"
        data = {'id': id}
        return self.db.query_db(query, data)

    def update_user_info(self, user_info):
        query = "UPDATE users SET first_name = :fname, last_name = :lname, email = :email, updated_on = now() WHERE id = :id"
        data = {
                'fname': user_info['fname'],
                'lname': user_info['lname'],
                'email': user_info['email'],
                'id': user_info['id'],
                }
        self.db.query_db(query, data)
        return user_info['id']

    def admin_update_user_info(self, user_info):
        query = "UPDATE users SET first_name = :fname, last_name = :lname, email = :email, access = :access, updated_on = now() WHERE id = :id"
        data = {
                'fname': user_info['fname'],
                'lname': user_info['lname'],
                'email': user_info['email'],
                'id': user_info['id'],
                'access': user_info['access']
                }
        self.db.query_db(query, data)
        return user_info['id']

    def update_user_description(self, user_info):
        query = "UPDATE users SET description = :description, updated_on = now() WHERE id = :user_id"
        data = {
                'description': user_info['description'],
                'user_id': user_info['id'],
                }
        self.db.query_db(query, data)
        return user_info['id']

    def update_user_password(self, user_info):
        errors = {}
        if len(user_info['password']) < 8:
            errors.update({'password': 'Password must be at least 8 characters'})
        elif not any(char.isdigit() for char in str(user_info['password'])):
            errors.update({'password': 'Password must contain at least one number'})
        elif not any(char.isupper() for char in str(user_info['password'])):
            errors.update({'password': 'Password must contain at least one uppercase letter'})
        if user_info['confirmpass'] != user_info['password']:
            errors.update({'confirmpass': 'The password confirmation does not match the password'})
        if len(errors) > 0:
            errors.update({'user_id': user_info['id']})
            return errors
        else:
            pw_hash = self.bcrypt.generate_password_hash(user_info['password'])
            query = "UPDATE users SET password = :password, updated_on = now() WHERE id = :user_id"
            data = {
                    'password': pw_hash,
                    'user_id': user_info['id'],
                    }
            self.db.query_db(query, data)
            return {'id': user_info['id']}
    

    def remove_user(self, id):
        query1 = 'DELETE FROM comments WHERE c_author_id = :id'
        query2 = 'DELETE FROM messages WHERE m_author_id = :id'
        query3 = 'DELETE FROM users WHERE id = :id'
        data = {'id': id}
        self.db.query_db(query1, data)
        self.db.query_db(query2, data)
        self.db.query_db(query3, data)
        return

    def get_messages(self, id):
        query = 'SELECT messages.id as m_id, message, messages.created_on as m_created_on, wall_id, users.first_name, users.last_name FROM dashboard.messages JOIN users ON m_author_id = users.id WHERE wall_id = :id ORDER BY m_created_on DESC'
        data = {'id': id}
        return self.db.query_db(query, data)

    def add_message(self, info):
        query = 'INSERT INTO messages(message, created_on, updated_on, m_author_id, wall_id) VALUES(:message, now(), now(), :m_author_id, :wall_id)'
        data = {
                'message': info['message'],
                'm_author_id': info['m_author_id'],
                'wall_id': info['wall_id']
                }
        self.db.query_db(query, data)                
        return info['wall_id']

    def get_comments(self, id):
        query = 'SELECT comments.id as c_id, comment, comments.created_on as c_created_on, c_message_id, wall_id, users.first_name, users.last_name FROM comments JOIN users on c_author_id = users.id WHERE wall_id = :id ORDER BY comments.created_on DESC'
        data = {'id': id}
        return self.db.query_db(query, data)

    def add_comment(self, info, id):
        query = 'INSERT INTO comments(comment, created_on, updated_on, c_author_id, c_message_id, wall_id) VALUES(:comment, now(), now(), :c_author_id, :c_message_id, :wall_id)'
        data = {
                'comment': info['comment'],
                'c_author_id': info['c_author_id'],
                'c_message_id': id,
                'wall_id': info['wall_id']
                }
        self.db.query_db(query, data)        
        return info['wall_id']