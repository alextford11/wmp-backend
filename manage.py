import json

import typer

from src.database import get_session
from src.models import Muscle, Workout

app = typer.Typer()


@app.command()
def hello_world():
    # need to have at least two commands, remove this once we have more commands than just build workouts
    typer.echo('Hello')


@app.command()
def build_workouts():
    typer.echo('Creating workouts and muscles')
    with open('./data/workouts.json') as f:
        data = json.load(f)

    muscles = data['muscles']
    muscle_obj_lu = {}
    workouts = data['workouts']

    db = get_session()()
    created_count, updated_count = 0, 0
    for muscle_var_name, muscle_name in muscles.items():
        muscle_obj, created = Muscle.manager(db).get_or_create(name=muscle_name)
        muscle_obj_lu[muscle_var_name] = muscle_obj
        if created:
            created_count += 1
        else:
            updated_count += 1
    typer.echo(f'Created {created_count}, updated {updated_count} Muscles')

    created_count, updated_count = 0, 0
    for workout in workouts:
        workout_obj, created = Workout.manager(db).get_or_create(name=workout['name'])
        for muscle_var in workout['muscles']:
            workout_obj.related_muscles.append(muscle_obj_lu[muscle_var])
        Workout.manager(db).update(workout_obj)
        if created:
            created_count += 1
        else:
            updated_count += 1
    typer.echo(f'Created {created_count}, updated {updated_count} Workouts')


if __name__ == '__main__':
    app()
