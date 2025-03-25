import logging.config
from sqlalchemy import *
from sqlalchemy.orm import *
from email.mime.text import MIMEText
import os
import logging
import smtplib

#__all__ = ['dev', 'dataTool',]


class dev():
    logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
    def engine(engine_sesion):
        return create_engine(engine_sesion)
    
    def session(engine_sesion):
        return sessionmaker(bind=engine_sesion)
    
    def base():
        return declarative_base()
    
    def metadata(base, engine):
        base.metadata.create_all(engine)
    
    def add_commit(session, user):
        session.add(user)
        session.commit()
    
    def _Column(*args, **kwargs):
        column = Column(*args, **kwargs)
        return column
    
    @staticmethod
    def Integer():
        return Integer()
    
    @staticmethod
    def String(length):
        return String(length)

class dataTool():
    def dell(file):
        os.remove(file)
    
    def read_data(session, model):
        data = session.query(model).all()
        for item in data:
            print(item)
    def connet(file,name):
        file = open(file, 'w')
        file.write(name)
        file.close()
    def email_send(subject,to,from_):
        msg = MIMEText(subject)
        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to
        
        # Add SMTP server connection and sending
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_, input("Enter password: "))  # Prompt for password securely
            server.send_message(msg)
            print(f"Email sent successfully to {to}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
        finally:
            server.quit()
    
    @staticmethod
    def _inter(app_name, route, db_path, port=3000, model_path=None, model_class=None):
        """Create Flask interface for database viewing
        Args:
            app_name: Flask app name
            route: URL endpoint
            db_path: Database file path
            port: Server port (default: 3000)
            model_path: Optional path to model module
            model_class: Optional model class to use directly
        """
        from flask import Flask, render_template, redirect
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        import importlib.util
        
        app = Flask(app_name, template_folder='templates')
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)

        _flask_run = app.run

        def load_model():
            # If model class provided directly, use it
            if model_class is not None:
                return model_class
                
            # Try loading from model_path if provided
            if model_path:
                try:
                    module_name, class_name = model_path.rsplit('.', 1)
                    spec = importlib.util.find_spec(module_name)
                    if spec is None:
                        print(f"Module {module_name} not found")
                        return None
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return getattr(module, class_name)
                except Exception as e:
                    print(f"Error loading model from {model_path}: {e}")
                    return None
            
            print("No model class or path provided")
            return None

        @app.route('/')
        def index():
            if route == '/':
                return serve_db()  # If route is root, serve directly
            return redirect(route)  # Otherwise redirect

        @app.route(route)
        def serve_db():
            try:
                model = load_model()
                if model is None:
                    error_msg = "Could not load database model. Check if tester.py exists with data class."
                    print(error_msg)
                    return error_msg, 500
                
                session = Session()
                records = session.query(model).all()
                if not records:
                    return "No records found in database", 404
                    
                return render_template('data.html', data=records)
            except Exception as e:
                error_msg = f"Database error: {str(e)}"
                print(error_msg)
                return error_msg, 500
            finally:
                session.close()
        
        def run(**kwargs):
            print(f"\nStarting server at: http://localhost:{port}")
            kwargs.setdefault('port', port)
            kwargs.setdefault('debug', True)
            kwargs.setdefault('host', '0.0.0.0')  # Allow external access
            kwargs.setdefault('use_reloader', False)
            _flask_run(**kwargs)  # Use stored Flask run method
        
        app.run = run
        return app

