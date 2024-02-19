from dbm import error
import openai
from dotenv import find_dotenv, load_dotenv
import os
import time
import logging
from datetime import datetime


from openai.types.beta import Assistant, Thread
from openai.types.beta.threads import Run, ThreadMessage

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

model = 'gpt-3.5-turbo-16k'

#== Create our Assistant ==#

personal_trainer_assistant: Assistant = client.beta.assistants.create(
    name='Personal Trainer',
    instructions= ''' You are the best personal trainer and nutritionist who knows how to get clients to build lean muscles. You have trained high-caliber athletes and movie stars''',
    model = model
)

assistant_id: str = personal_trainer_assistant.id

print(f"Personal Trainer Id: {personal_trainer_assistant.id}")

#== Step 2: Create a thread ==#

thread: Thread = client.beta.threads.create(
    messages = [
        {
            'role': 'user',
            'content': 'How do I get started working out to lose fat and built muscles'
        }
    ]
)

thread_id: str = thread.id

print(f"Thread Id: {thread_id}")

#== Step 3: Create a Message ==#

message: str = 'What are the best exercise for lean muscles and getting strong'

new_message: ThreadMessage = client.beta.threads.messages.create(
    thread_id = thread_id,
    role='user',
    content= message
)

#== Step 4: Run our Assistant ==#
run: Run = client.beta.threads.runs.create(
    thread_id = thread_id,
    assistant_id=assistant_id,
    instructions='Please address the user as James Bond'
)
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id = run_id)
            if run.completed_at:
                elapased_time = run.completed_at - run.created_at
                formatted_elapased_time = time.strftime(
                    '%H:%M:%S', time.gmtime(elapased_time)
                )
                print(f"Run completed in {formatted_elapased_time}")
                logging.info(f"Run completed in {formatted_elapased_time}.")
                
                messages = client.beta.threads.messages.list(thread_id = thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)
            
# == Run ==#

wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)
                