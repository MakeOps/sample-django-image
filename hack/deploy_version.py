#!/usr/bin/env python3

import argparse
import boto3
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-task-definition', required=True,
                      help='Name of the source task definition')
    parser.add_argument('--output', required=True,
                      help='Path to the output task definition file')
    return parser.parse_args()


def describe_task_definition(task_def_name):
    ecs = boto3.client('ecs')
    print(f'Describing task definition: {task_def_name}')
    response = ecs.describe_task_definition(taskDefinition=task_def_name)
    return response['taskDefinition']


def map_task_definition(task_def):
    # Create a copy of the task definition
    new_task_def = task_def.copy()

    # Remove fields that shouldn't be included in new task definition
    fields_to_remove = [
        'taskDefinitionArn',
        'revision',
        'status',
        'requiresAttributes',
        'registeredAt',
        'registeredBy'
    ]

    for field in fields_to_remove:
        new_task_def.pop(field, None)

    # For container definitions, preserve everything except image
    for container in new_task_def.get('containerDefinitions', []):
        container['image'] = '<IMAGE_NAME>'
        if 'memoryReservation' not in container or 'memory' not in container:
            if 'memory' in new_task_def:
                container['memoryReservation'] = int(new_task_def['memory'])
            else:
                container['memoryReservation'] = 512

    return new_task_def

def write_task_definition(task_def, output_path):
    with open(output_path, 'w') as f:
        json.dump(task_def, f, indent=4)

def main():
    args = parse_args()

    # Get the current task definition
    task_def = describe_task_definition(args.source_task_definition)

    # Map to new format
    new_task_def = map_task_definition(task_def)

    # Register the task definition
    write_task_definition(new_task_def, args.output)

    print(f'Task definition written to {args.output}')


if __name__ == '__main__':
    main()
