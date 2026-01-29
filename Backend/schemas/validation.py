from pydantic import BaseModel,Field,computed_field,field_validator,model_validator
from typing import Annotated,Literal
import numpy as np

teams=['Royal Challengers Bengaluru', 'Punjab Kings', 'Delhi Capitals',
       'Mumbai Indians', 'Kolkata Knight Riders', 'Rajasthan Royals',
       'Sunrisers Hyderabad', 'Chennai Super Kings', 'Gujarat Titans',
       'Lucknow Super Giants']

cities=['Mumbai', 'Bangalore', 'Centurion', 'Jaipur', 'Durban', 'Kolkata',
       'Bloemfontein', 'Delhi', 'Hyderabad', 'Chennai', 'Johannesburg',
       'Port Elizabeth', 'Ahmedabad', 'Cape Town', 'Pune', 'Nagpur',
       'Kimberley', 'Cuttack', 'Visakhapatnam', 'East London']

class Input(BaseModel):
    batting_team:Annotated[Literal['Royal Challengers Bengaluru', 'Punjab Kings', 'Delhi Capitals',
       'Mumbai Indians', 'Kolkata Knight Riders', 'Rajasthan Royals',
       'Sunrisers Hyderabad', 'Chennai Super Kings', 'Gujarat Titans',
       'Lucknow Super Giants'],Field(..., description="The batting Team for match", title='Batting Team')]
    
    bowling_team:Annotated[Literal['Royal Challengers Bengaluru', 'Punjab Kings', 'Delhi Capitals',
       'Mumbai Indians', 'Kolkata Knight Riders', 'Rajasthan Royals',
       'Sunrisers Hyderabad', 'Chennai Super Kings', 'Gujarat Titans',
       'Lucknow Super Giants'],Field(..., description="The batting Team for match", title='Batting Team')]
    
    city:Annotated[Literal['Mumbai', 'Bangalore', 'Centurion', 'Jaipur', 'Durban', 'Kolkata',
       'Bloemfontein', 'Delhi', 'Hyderabad', 'Chennai', 'Johannesburg',
       'Port Elizabeth', 'Ahmedabad', 'Cape Town', 'Pune', 'Nagpur',
       'Kimberley', 'Cuttack', 'Visakhapatnam', 'East London'],Field(..., description="The batting Team for match", title='Batting Team')]
    
    over:Annotated[float,Field(..., description="The Over Till now completed", title='Over Completed',le=20)]
    target:Annotated[int,Field(..., description="The target for second team", title='Target in Match')]
    score:Annotated[int,Field(..., description="The Score till now in match", title='Score of Match')]
    wicket:Annotated[int,Field(..., description="The wicket gone in match", title='Wicket Gone',le=10)]


    @field_validator('batting_team',mode='before')
    @classmethod
    def team_batting(cls,value):
        return value.strip().title()
       
    @field_validator('city',mode='before')
    @classmethod
    def city(cls,value):
        return value.strip().title()
    
    @field_validator('bowling_team',mode='before')
    @classmethod
    def team_bowling(cls,value):
        return value.strip().title()

    @field_validator('over')
    @classmethod
    def validate_over(cls,value):
        over=int(value)
        decimalpart=np.round((value-over)*10,0)
        if decimalpart>6:
            raise ValueError("Decimal Part can't be greater than 6")
        return value

    @model_validator(mode='after')
    def check_team(cls,model):
        if model.batting_team == model.bowling_team:
            return ValueError("Batting and Bowling Team can't be same")
        return model

    @computed_field
    @property
    def runs_left(self)->int:
        return self.target-self.score
    

    @computed_field
    @property
    def ball_left(self)->int:
        over=int(self.over)
        balls=int(np.round((self.over-over)*10,0))
        total_balls=over*6+balls
        return 120-total_balls
    
    @computed_field
    @property
    def wicket_left(self)->int:
        return 10-self.wicket
    
    @computed_field
    @property
    def crr(self)->float:
        return np.round((self.score*6)/(120-self.ball_left),2)
    
    @computed_field
    @property
    def rrr(self)->float:
        return np.round((self.runs_left*6)/(self.ball_left),2)



#TEsting data
'''
test={
    'batting_team':'royal Challengers Bengaluru',
    'bowling_team':"Delhi Capitals",
    'city':"mumbai",
    'over':11.6,
    'target':120,
    "score":60,
    "wicket":11
}

obj1=input(**test)

print(obj1.model_dump())

'''