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
    created_count, unchanged_count = 0, 0
    for muscle_var_name, muscle_name in muscles.items():
        muscle_obj, created = Muscle.manager(db).get_or_create(name=muscle_name)
        muscle_obj_lu[muscle_var_name] = muscle_obj
        if created:
            created_count += 1
        else:
            unchanged_count += 1
    typer.echo(f'Created {created_count}, {unchanged_count} Muscles left unchanged')

    created_count, updated_count, unchanged_count = 0, 0, 0
    for workout in workouts:
        updated = False
        workout_obj, created = Workout.manager(db).get_or_create(name=workout['name'])
        related_muscles = workout_obj.related_muscles
        for muscle_var in workout['muscles']:
            if (muscle := muscle_obj_lu[muscle_var]) not in related_muscles:
                updated = not created
                workout_obj.related_muscles.append(muscle)
        Workout.manager(db).update(workout_obj)
        if created:
            created_count += 1
        elif updated:
            updated_count += 1
        else:
            unchanged_count += 1
    typer.echo(f'Created {created_count}, updated {updated_count} Workouts, {unchanged_count} Muscles left unchanged')


if __name__ == '__main__':
    app()
