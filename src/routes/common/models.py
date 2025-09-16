from datetime import datetime

from ... import db


class VisitCounter(db.Model):
    __tablename__ = "RouteVisits"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)   # ISO year
    week = db.Column(db.Integer, nullable=False)   # ISO week (1–53)
    count = db.Column(db.Integer, default=0)
    route = db.Column(db.String, nullable=True, default="N/A")

    __table_args__ = (db.UniqueConstraint('year', 'week', name='_year_week_uc'),)


# def count_visit(route):
    
#     now = datetime.now()
#     iso_year, iso_week, _ = now.isocalendar()
#     counter = VisitCounter.query.filter_by(year=iso_year, week=iso_week, route=route).first()

#     if not counter:
#         counter = VisitCounter(year=iso_year, week=iso_week, route=route, count=1)
#         db.session.add(counter)
#     else:
#         counter.count += 1
    
#     db.session.commit()

from functools import wraps

def count_visit(route: str):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = datetime.now()
            iso_year, iso_week, _ = now.isocalendar()

            counter = VisitCounter.query.filter_by(
                year=iso_year, week=iso_week, route=route
            ).first()

            if not counter:
                counter = VisitCounter(year=iso_year, week=iso_week, route=route, count=1)
                db.session.add(counter)
            else:
                counter.count += 1

            db.session.commit()
            return f(*args, **kwargs)
        return wrapped
    return decorator