from .models import World, Character, Scene, Location

def get_user_world_stats(user):
    worlds = World.objects.filter(user=user)

    worlds_stats = []
    characters = 0
    scenes = 0
    locations = 0

    for world in worlds:
        character_count = world.characters.count()
        scene_count = Scene.objects.filter(location__world=world).count()
        location_count = world.locations.count()

        characters += character_count
        scenes += scene_count
        locations += location_count

        worlds_stats.append({
            'id': world.id,
            'name': world.name,
            'character_count': character_count,
            'scene_count': scene_count,
            'location_count': location_count
        })

    return {
        'worlds': worlds_stats,
        'worlds_count': len(worlds),
        'characters': characters,
        'scenes': scenes,
        'locations': locations
    }