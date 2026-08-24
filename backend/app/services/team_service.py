from app.models.teams import Team,TeamMembership
from app.models.users import User
from app import db
from app.utils.validators import validate_input


class TeamService:
    
    @staticmethod 
    def create_team(data, user_id):
        error = validate_input(data,['name'])
        
        if error:
            return {'status': 'invalid', 'message': 'error'}
        
        existing  = Team.query.filter_by(name =data['name']).first()
        
        if existing:
            return {'status': 'duplicate', "message": "A team wiht this name already exist"}

        team  =Team(
                name = data['name'],
                description = data.get('description')
        )        
        
        db.session.add(team)
        db.session.flush()
        
        return {'Status': "success", "tean": team.to_dict()}
    
    @staticmethod
    def get_team(team_id, requesting_user_id):
        team = db.session.get(Team, team_id)
        
        if team is None:
            return{"status": "not_found"}
        
        membership = TeamMembership.query.filter_by(team_id = team_id, user_id = requesting_user_id)
        
        if not membership:
            return {"status": "unauthorized"}
        
        members = TeamMembership.query.filter_by(team_id = team_id).all()
        
        return{ 'status' : "success",
               "team": team.to_dict(),
               "members": [m.to_dict( ) for m in members]}
        
        