# scenes.py (Visual Novel Data Structure)

story = {
    "start": [
        {
            "background_img": "space_station.bmp",
            "character_img": "nova_neutral.bmp",
            "position": "left",
            "name": "Nova",
            "text": "The engine logs are flashing red. We don't have much fuel left, Orion."
        },
        {
            "character_img": "orion_serious.bmp",
            "position": "right",
            "name": "Orion",
            "text": "If we search the cargo hold, we might find a reserve cell. Are you going to help me look?"
        },
        {
            "name": "System",
            "text": "Decide how Nova responds to Orion's request.",
            "choices": [
                {
                    "text": "Search the toxic cargo hold fearlessly.",
                    "set_flag": {"brave": True},
                    "next_scene": "cargo_hold"
                },
                {
                    "text": "Stay at the primary control console.",
                    "set_flag": {"brave": False},
                    "next_scene": "control_room"
                }
            ]
        }
    ],

    "cargo_hold": [
        {
            "background_img": "cargo_bay.bmp",
            "character_img": "nova_determined.bmp",
            "position": "left",
            "name": "Nova",
            "text": "It's pitch black down here, but I found an ancient backup core!"
        },
        {
            "character_img": "orion_happy.bmp",
            "position": "right",
            "name": "Orion",
            "text": "Excellent work. Let's make our way back to the bridge immediately."
        },
        {
            "name": "System",
            "text": "You head back to the main terminal with the core in hand.",
            "choices": [
                {
                    "text": "Proceed to the destination platform.",
                    "next_scene": "bridge_confrontation"
                }
            ]
        }
    ],

    "control_room": [
        {
            "background_img": "control_deck.bmp",
            "character_img": "nova_nervous.bmp",
            "position": "left",
            "name": "Nova",
            "text": "I stayed behind, but the control monitors are fluctuating violently."
        },
        {
            "name": "System",
            "text": "Orion returns empty-handed and sighs heavily.",
            "choices": [
                {
                    "text": "Face whatever is approaching the ship.",
                    "next_scene": "bridge_confrontation"
                }
            ]
        }
    ],

    "bridge_confrontation": [
        {
            "background_img": "bridge_window.bmp",
            "character_img": "orion_panicked.bmp",
            "position": "right",
            "name": "Orion",
            "text": "A pirate interceptor just dropped out of warp right in front of us!"
        },
        {
            "name": "System",
            "text": "The interceptor demands a total surrender of your vessel.",
            "choices": [
                {
                    "text": "Surrender and offer them your remaining rations.",
                    "next_scene": "bad_ending"
                },
                {
                    "text": "Route emergency auxiliary power to the shield array.",
                    "next_scene": "good_ending"
                },
                {
                    "text": "[REQUISITION] Overcharge systems using your brave cargo-hold core!",
                    "req_flag": {"brave": True},
                    "next_scene": "secret_ending"
                }
            ]
        }
    ],

    "bad_ending": [
        {
            "background_img": "black_screen.bmp",
            "name": "Ending",
            "text": "You surrendered. The ship was impounded, leaving you stranded out in deep space. Game Over."
        }
    ],

    "good_ending": [
        {
            "background_img": "galaxy.bmp",
            "character_img": "nova_happy.bmp",
            "position": "left",
            "name": "Nova",
            "text": "The shields held up! We safely drifted past their scanning radar range."
        },
        {
            "name": "Ending",
            "text": "You managed to survive the encounter and made it safely to port. Victory!"
        }
    ],

    "secret_ending": [
        {
            "background_img": "explosion.bmp",
            "character_img": "orion_happy.bmp",
            "position": "right",
            "name": "Orion",
            "text": "Incredible! That backup core completely vaporized their tracking array!"
        },
        {
            "name": "Ending",
            "text": "You successfully saved the crew, defeated the interceptor, and unlocked the true ending!"
        }
    ]
}
