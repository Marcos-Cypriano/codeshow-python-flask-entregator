import datetime
from flask import current_app
from flask_apscheduler import APScheduler as _BaseAPScheduler
from entregator.ext.db import db
from entregator.ext.db.models import Order


class APScheduler(_BaseAPScheduler):
    def get_app(self):
        if self.app:
            return self.app
        else:
            return current_app
    def run_job(self, id, jobstore=None):
        with self.app.app_context():
            super().run_job(id=id, jobstore=jobstore)
            

scheduler = APScheduler()

def expirer_order() -> Order:
    with scheduler.app.app_context():
        deadline = datetime.datetime.now() - datetime.timedelta(minutes=30)
        orders = Order.query.filter(Order.created_at < deadline, Order.completed == 0).all()
        for order in orders:
            order.expired = 1
            db.session.commit()

    return f'{len(orders)} pedidos foram expirados.'

def init_app(app):
    scheduler.init_app(app)
    scheduler.add_job(id='Scheduled DB Cleaning',func=expirer_order, trigger="interval", minutes=5)
    scheduler.start()

    # atexit.register(lambda: scheduler.shutdown())