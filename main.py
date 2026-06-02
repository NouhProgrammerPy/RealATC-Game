from classes import *

if __name__ == "__main__":
    textures_dict = {"VOR/DME": "texture3.png", "WAYPOINT": "texture1.png"}
    screen = pygame.display.set_mode((900, 900))
    score = 0
    airplanes = []
    waypoints = []
    runways = []
    waypoints.append(Waypoint(270, 500, "WAYPOINT", "MOGAV", textures_dict))
    waypoints.append(Waypoint(300, 200, "WAYPOINT", "TOSBO", textures_dict))
    waypoints.append(Waypoint(500, 300, "VOR/DME", "SHJ", textures_dict))
    waypoints.append(Waypoint(470, 350, "WAYPOINT", "LADVI", textures_dict))
    waypoints.append(Waypoint(600, 450, "WAYPOINT", "BUBOK", textures_dict))
    waypoints.append(Waypoint(620, 200, "WAYPOINT", "RAGSO", textures_dict))
    runways.append(Runway(400, 400, ["12R", "30L"], "texture2.png"))
    runways.append(Runway(410, 420, ["12L", "30R"], "texture2.png"))
    clock = pygame.time.Clock()
    delta_time = clock.tick(500) / 1000
    warner = DistanceWarner()
    airplane_spawner = AirplaneSpawner(30, 10)
    running = True
    cmd_mode = False
    cmd_callsign = ""
    cmd = ""
    cmd_text = ""
    spawn_timer = 29
    start_time = pygame.time.get_ticks()
    while running:
        screen.fill((0, 0, 0))
        time_ms = pygame.time.get_ticks()
        top_bar = font.render(
            f"FPS: {int(clock.get_fps())}      Time (s): {round(time_ms / 1000)}      Score: {score}      Airplane Count: {len(airplanes)}",
            True, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for airplane in airplanes:
                    plane_rect = pygame.Rect(airplane.x_pos, airplane.y_pos, 50, 50)
                    if plane_rect.collidepoint(mouse_pos):
                        cmd_mode = True
                        cmd_callsign = airplane.callsign
                        break
            if cmd_mode:
                if event.type == pygame.KEYDOWN:
                    if cmd == "":
                        if event.key == pygame.K_h:
                            cmd = "Head."
                            break
                        if event.key == pygame.K_a:
                            cmd = "Alt."
                            break
                        if event.key == pygame.K_s:
                            cmd = "Spd."
                            break
                        if event.key == pygame.K_w:
                            cmd = "Wypt."
                            break
                        if event.key == pygame.K_l:
                            cmd = "Lnd."
                            break
                        if event.key == pygame.K_t:
                            cmd = "TOF"
                            break
                        if event.key == pygame.K_d:
                            cmd = "Hold"
                            break
                        if event.key == pygame.K_BACKSPACE:
                            cmd = ""
                            cmd_callsign = ""
                            cmd_mode = False
                    if cmd is not None:
                        if event.key == pygame.K_RETURN:
                            update_cmd(cmd, cmd_text, cmd_callsign, airplanes)
                            cmd_mode = False
                            cmd_text = ""
                            cmd = ""
                            cmd_callsign = ""
                        elif event.key == pygame.K_BACKSPACE:
                            if cmd_text != "":
                                cmd_text = cmd_text[:-1]
                            elif cmd_text == "":
                                cmd = ""
                                cmd_callsign = ""
                                cmd_mode = False
                        elif event.unicode:
                            cmd_text += event.unicode
        spawn_timer += delta_time
        if spawn_timer >= airplane_spawner.cooldown_s and len(airplanes) < airplane_spawner.max_airplanes:
            airplanes.append(airplane_spawner.new_plane())
            spawn_timer = 0
        for waypoint in waypoints:
            screen.blit(waypoint.surface, (waypoint.x_pos, waypoint.y_pos))
        for runway in runways:
            screen.blit(runway.surface, runway.rect)
        for airplane in airplanes:
            score += airplane.reload_position(delta_time, waypoints, runways)
            for i in range(1, len(airplane.trail)):
                if airplane.opacity:
                    pygame.draw.line(screen, (180, 180, 180),
                                     airplane.trail[i - 1],
                                     airplane.trail[i], 2)
            screen.blit(airplane.reload_surface(), (airplane.x_pos, airplane.y_pos))
            if airplane.pop:
                airplanes.pop(airplanes.index(airplane))
        if warner.check(airplanes):
            running = False  # GAME OVER
        if cmd_mode:
            cmd_text_surface = font.render(
                f"{cmd_callsign}:\n(H)eading\n(A)ltitude\n(W)aypoint\n(S)peed\n(L)and\n(T)akeoff\nHol(D)",
                True, (255, 255, 255))
            if cmd:
                cmd_text_surface = font.render(
                    f"{cmd_callsign}:\n{cmd}:\n{cmd_text}", True, (255, 255, 255))
            screen.blit(cmd_text_surface, (850, 800))
        screen.blit(top_bar, (10, 10))
        pygame.display.flip()
        delta_time = clock.tick(500) / 1000
        delta_time = max(0.0001, min(0.1, delta_time))

    pygame.quit()
