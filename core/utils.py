import os


def resolve_asset_path(asset_path: str):
    if not asset_path:
        return None

    candidate = asset_path if os.path.isabs(asset_path) else os.path.join(os.path.dirname(__file__), '..', asset_path)
    candidate = os.path.normpath(candidate)
    return candidate if os.path.exists(candidate) else None


def format_list(items):
    return '\n'.join(f'• {item}' for item in items)


def format_teams(teams):
    return '\n'.join(f'{team.get("type")} • {team.get("members")}' for team in teams)
