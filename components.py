from worlds.LauncherComponents import Component, Type, components, launch

from .data.Strings import APConsole, Meta

def run_client(*args: str) -> None:
    from .AE3_Client import launch_init

    launch(launch_init, name=APConsole.Info.client_name.value, args=args)

components.append(
        Component(
            APConsole.Info.client_name.value,
            func=run_client,
            game_name=Meta.game,
            component_type=Type.CLIENT,
            supports_uri=True,
        )
    )

