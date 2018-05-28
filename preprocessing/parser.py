# -*- coding: utf-8 -*-

import json
import csv
from entities.dependency import Dependency
from entities.participation import Participation
from entities.requirement import Requirement


def parse_requirements(path):
    with open(path) as f:
        json_string = f.read()
        raw_requirement_list = json.loads(json_string)
        return map(lambda raw_requirement:
                   Requirement(int(raw_requirement['id']), raw_requirement['title'], raw_requirement['description']),
                   raw_requirement_list)


def parse_dependencies_of_example_solution(path, requirements):
    assert isinstance(requirements, list)
    with open(path) as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        dependencies_of_solution = []
        for row in reader:
            if len(row) == 5:
                # ID,Title,Requires,Incompatible with,Additional requires
                rx, _, require_ry_str, incompatible_ry_str, _ = row
            else:
                # ID,Title,Requires,Imcompatible with
                rx, _, require_ry_str, incompatible_ry_str = row
            if len(require_ry_str) > 0:
                dependencies_of_solution += map(
                    lambda ry: Dependency(int(rx.strip()), int(ry.strip().replace('R', '')), 1, requirements),
                    require_ry_str.split(';')
                )
            if len(incompatible_ry_str) > 0:
                dependencies_of_solution += map(
                    lambda ry: Dependency(int(rx.strip()), int(ry.strip().replace('R', '')), 2, requirements),
                    incompatible_ry_str.split(';')
                )
        return dependencies_of_solution


def parse_participations_and_dependencies_of_student_solutions(path, requirements):
    assert isinstance(requirements, list)
    with open(path) as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        participations = {}
        for row in reader:
            participation_id, ip_address, ticket_code, datetime, sequence_ordering, _, rx_id, dependency_type, ry_id = row
            if participation_id not in participations:
                participations[participation_id] = Participation(int(participation_id), ip_address, ticket_code, datetime, sequence_ordering)
            dependency = Dependency(rx_id, ry_id, dependency_type, requirements)
            participations[participation_id].add_dependency(dependency)
        return participations

