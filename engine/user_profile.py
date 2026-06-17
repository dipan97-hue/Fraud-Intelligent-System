from faker import Faker
import random
import uuid

fake = Faker()

def create_profile(num_user = 100):

    users = []

    for _ in range(num_user):

        users.append({
            'user_id':fake.uuid4(),
            'username':fake.name(),
            'home_country': fake.country(),
            'avg_amount': random.randint(50,500),
            'preferred_device': random.choice(['mobile','web','tablet']),
            
        })

    return users





