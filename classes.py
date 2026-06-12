import pygame
import math
from random import choice, randint

pygame.init()

font = pygame.font.Font(None, 12)


def update_cmd(cmd, value, airplane_callsign, airplane_list):
    for airplane in airplane_list:
        if airplane.callsign == airplane_callsign:
            target = airplane
            break
    match cmd:
        case "Head.":
            value = int(value)
            if value > 360 or value < 0:
                raise ValueError(
                    "Yes, this game crashes if you tell an airplane to go to an impossible heading, I might change it later, but now it is what it is.")
            target.new_instructions(new_heading=value, new_status="Cruise")
            target.waypoint_name = ""
        case "Alt.":
            value = int(value)
            if value > 40000 or value < 0:
                raise ValueError(
                    "Yes, this game crashes if you tell an airplane to go to an impossible altitude, I might change it later, but now it is what it is.")
            target.new_instructions(new_altitude=value,
                                    new_status="Cruise" if target.targets["Status"] != "Hold" else "Hold")
        case "Spd.":
            value = int(value)
            if value > 400 or value < 50:
                raise ValueError(
                    "Yes, this game crashes if you tell an airplane to go to an impossible speed, I might change it later, but now it is what it is.")
            target.new_instructions(new_speed=value,
                                    new_status="Cruise" if target.targets["Status"] != "Hold" else "Hold")
        case "Wypt.":
            target.new_instructions(new_waypoint=value.upper(), new_status="Cruise")
            target.waypoint_name = ""
        case "Lnd.":
            target.new_instructions(new_heading=target.heading)
            runway_heading = int(value[:2]) * 10
            diff = (runway_heading - target.heading + 180) % 360 - 180
            if abs(diff) > 60 or target.altitude < 1000 or target.altitude > 3000 or target.speed > 250:
                return
            target.new_instructions(land=["Lnd", value.upper()])
        case "TOF":
            raise NotImplementedError("TOF still not implemented! For takeoff traffic, check versions v0.4+")
        case "Hold":
            if target.speed > 250:
                return
            target.before_hold_wpt = True
            target.new_instructions(new_status=f"Hold")
            target.waypoint_name = value.upper()[2:]
            target.hold_dir = value.upper()[0]
        case _:
            raise ValueError(
                "Internal Game Error, please open an issue on GitHub and paste the following:\nCMD NOT FOUND ERROR ( update_cmd() )")


class Airplane:
    def __init__(self, callsign, x_pos, y_pos, speed, heading, altitude: int, altitude_climb_rate_fpm,
                 texture, opacity: int = 1, max_trail_length: int = 1750):
        self.callsign = callsign
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.heading = heading
        self.altitude = altitude
        self.pop = False
        self.speed = speed
        self.trail = []
        self.climb_descent_sign = "="
        self.altitude_climb_rate_fpm = altitude_climb_rate_fpm
        self.max_trail_length = max_trail_length
        self.opacity = opacity
        self.texture = pygame.image.load(texture).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (10, 10))
        self.surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.near_col = False
        self.rect = None
        self.after_fix = False
        # HOLDING:##########
        self.before_hold_wpt = True
        self.hold_timer = 0
        self.hold_heading = 0
        self.hold_dir = "R"  # or "L"
        self.waypoint_name = ""
        ###################
        self.score_timer = 0
        self.targets = {
            "Waypoint": None,
            "Heading": self.heading,
            "Altitude": self.altitude,
            "Speed": self.speed,
            "Status": "Cruise"
        }

    def reload_surface(self):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.texture, (0, 40))
        if not self.near_col:
            if self.targets["Waypoint"]:
                text_surface = font.render(
                    f"{self.callsign}\n{round(self.heading)} / {self.targets["Waypoint"]}\n{self.climb_descent_sign} {round(self.altitude / 100)}  / {round(self.speed)}kt",
                    True,
                    (255, 255, 255))
            elif self.targets["Status"] != "Cruise":
                text_surface = font.render(
                    f"{self.callsign}\n{round(self.heading)} / {self.targets["Status"]}\n{self.climb_descent_sign} {round(self.altitude / 100)}  / {round(self.speed)}kt",
                    True,
                    (255, 255, 255))
            elif self.targets["Heading"] != self.heading:
                text_surface = font.render(
                    f"{self.callsign}\n{round(self.heading)} / {self.targets["Heading"]}\n{self.climb_descent_sign} {round(self.altitude / 100)}  / {round(self.speed)}kt",
                    True,
                    (255, 255, 255))
            else:
                text_surface = font.render(
                    f"{self.callsign}\n{round(self.heading)}\n{self.climb_descent_sign} {round(self.altitude / 100)}  / {round(self.speed)}kt",
                    True,
                    (255, 255, 255))
            pygame.draw.line(self.surface, (255, 255, 255, 100), (12, 38),
                             (text_surface.get_height() + 2, 50 - (text_surface.get_width() - 25)), 2)
        else:
            if self.targets["Waypoint"]:
                text_surface = font.render(
                    f"{self.callsign}\n{round(self.heading)} / {self.targets["Waypoint"]}\n{self.climb_descent_sign} {round(self.altitude / 100)}  / {round(self.speed)}kt",
                    True,
                    (255, 0, 0))
            elif self.targets["Status"] != "Cruise":
                text_surface = font.render(
                    f"{self.callsign}\n{round(self.heading)}\n{self.climb_descent_sign} {round(self.altitude / 100)}  / {round(self.speed)}kt",
                    True,
                    (255, 0, 0))
            elif self.targets["Heading"] != self.heading:
                text_surface = font.render(
                    f"{self.callsign}\n{round(self.heading)} / {self.targets["Heading"]}\n{self.climb_descent_sign} {round(self.altitude / 100)}  / {round(self.speed)}kt",
                    True,
                    (255, 0, 0))
            else:
                text_surface = font.render(
                    f"{self.callsign}\n{round(self.heading)}\n{self.climb_descent_sign} {round(self.altitude / 100)}  / {round(self.speed)}kt",
                    True,
                    (255, 0, 0))
            pygame.draw.line(self.surface, (255, 0, 0, 255), (12, 38),
                             (text_surface.get_height() + 2, 50 - (text_surface.get_width() - 25)), 2)
        self.surface.blit(text_surface, (50 - text_surface.get_width(), 0))
        if self.opacity:
            self.surface.set_alpha(255)
        else:
            self.surface.set_alpha(0)
        return self.surface

    def new_instructions(self, new_waypoint=None, new_heading=None, new_altitude=None, new_speed=None, new_status=None,
                         new_opacity=None, land=None):
        if new_waypoint:
            self.targets["Waypoint"] = new_waypoint
            self.targets["Heading"] = None
        elif new_heading is not None:
            self.targets["Heading"] = new_heading
            self.targets["Waypoint"] = None
        self.targets["Altitude"] = new_altitude if new_altitude is not None else self.targets["Altitude"]
        self.targets["Speed"] = new_speed if new_speed is not None else self.targets["Speed"]
        self.targets["Status"] = new_status if new_status else self.targets["Status"]
        self.targets = {
            "Waypoint": self.targets["Waypoint"],
            "Heading": self.heading,
            "Altitude": self.targets["Altitude"],
            "Speed": 160,
            "Status": f"Lnd  {land[1]}"
        } if land is not None else self.targets
        if new_opacity is not None:
            self.opacity = new_opacity

    def reload_position(self, delta_time, waypoint_list, runway_list):
        """
        To be called every frame reload, updates all positions.
        """
        score_change = 0
        if self.x_pos > 880 or self.x_pos < 0 or self.y_pos > 880 or self.y_pos < 0:
            self.pop = True
            score_change -= 200
            return score_change
        target_heading = self.heading
        landing = self.targets["Status"].startswith("Lnd")
        if landing:
            runway_name = self.targets["Status"][5:]
            runway = next((r for r in runway_list if runway_name in r.runways), None)
            if runway:
                idx = runway.runways.index(runway_name)
                tx, ty = runway.runway_coords[idx]
                runway_heading = int(runway_name[:2]) * 10
                rad = math.radians(runway_heading)
                fix_distance = 130
                back_dx = -math.sin(rad)
                back_dy = math.cos(rad)
                fix_x = tx + back_dx * fix_distance
                fix_y = ty + back_dy * fix_distance
                dx = fix_x - self.x_pos
                dy = fix_y - self.y_pos
                dist_to_fix = math.hypot(dx, dy)
                if dist_to_fix > 25 and not self.after_fix:
                    target_heading = (math.degrees(math.atan2(dx, -dy))) % 360
                else:
                    target_heading = runway_heading
                self.targets["Heading"] = target_heading
                if dist_to_fix < 100 and not self.after_fix:
                    self.new_instructions(new_speed=180, new_altitude=1000)
                if dist_to_fix < 50 and not self.after_fix:
                    self.after_fix = True
                    self.new_instructions(new_speed=170, new_altitude=800)
                if self.after_fix:
                    dx = tx - self.x_pos
                    dy = ty - self.y_pos
                    target_heading = (math.degrees(math.atan2(dx, -dy))) % 360
                    self.new_instructions(new_heading=target_heading)
                    dist = math.hypot(dx, dy)
                    if dist < 100:
                        self.new_instructions(new_speed=150, new_altitude=400)
                    if dist < 60:
                        self.new_instructions(new_speed=130, new_altitude=100)
                    if dist < 10:
                        self.new_instructions(new_altitude=34)
                        self.targets["Status"] = "Landed"
        if self.targets["Status"] == "Landed":
            self.altitude = 34
            self.new_instructions(new_speed=0, new_altitude=34)
            if self.speed < 10:
                self.pop = True
                score_change += 150
        if self.targets["Waypoint"]:
            waypoint_found = False
            for waypoint in waypoint_list:
                if waypoint.name == self.targets["Waypoint"]:
                    waypoint_x = waypoint.x_pos
                    waypoint_y = waypoint.y_pos
                    waypoint_found = True
                    break
            if waypoint_found:
                dx = (waypoint_x + 5) - (self.x_pos + 5)
                dy = (waypoint_y + 15) - (self.y_pos + 45)
                target_heading = (math.degrees(math.atan2(dx, -dy))) % 360
                if math.hypot(dx, dy) < 10:
                    self.new_instructions(new_heading=target_heading)
            else:
                self.new_instructions(new_heading=target_heading)
        elif self.targets["Heading"] is not None:
            target_heading = self.targets["Heading"]
        if self.targets["Status"] == "Hold":
            if self.speed > 250:
                self.new_instructions(new_status="Cruise")
            waypoint_name = self.waypoint_name
            if self.before_hold_wpt:
                waypoint_found = False
                for waypoint in waypoint_list:
                    if waypoint.name == waypoint_name:
                        waypoint_x = waypoint.x_pos
                        waypoint_y = waypoint.y_pos
                        waypoint_found = True
                        break
                if self.hold_dir == "" or self.hold_dir is None:
                    waypoint_found = False
                if waypoint_found:
                    dx = (waypoint_x + 5) - (self.x_pos + 5)
                    dy = (waypoint_y + 15) - (self.y_pos + 45)
                    target_heading = (math.degrees(math.atan2(dx, -dy))) % 360
                    self.new_instructions(new_heading=target_heading)
                    if math.hypot(dx, dy) < 10:
                        self.before_hold_wpt = False
                        self.hold_heading = self.heading
                        self.holding_phase = "outbound"
                        self.hold_timer = 0
                else:
                    self.new_instructions(new_status="Cruise", new_heading=self.heading)
            else:
                self.hold_timer += delta_time
                if self.holding_phase == "outbound":
                    if self.hold_dir == "R":
                        target_heading = target_heading = (self.hold_heading + 179) % 360
                        if self.hold_timer >= 5:
                            target_heading = target_heading = (self.hold_heading + 181) % 360
                    if self.hold_dir == "L":
                        target_heading = target_heading = (self.hold_heading - 179) % 360
                        if self.hold_timer >= 5:
                            target_heading = target_heading = (self.hold_heading - 181) % 360
                    self.new_instructions(new_heading=target_heading)
                    if self.hold_timer >= 65:
                        self.hold_timer = 0
                        self.holding_phase = "inbound"
                elif self.holding_phase == "inbound":
                    target_heading = self.hold_heading
                    self.new_instructions(new_heading=target_heading)
                    if self.hold_timer >= 65:
                        self.hold_timer = 0
                        self.holding_phase = "outbound"
        self.trail.append((self.x_pos + 5, self.y_pos + 45))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        difference = self.targets["Altitude"] - self.altitude
        step = self.altitude_climb_rate_fpm * delta_time / 60
        if abs(difference) <= step:
            self.climb_descent_sign = "="
            self.altitude = self.targets["Altitude"]
        else:
            if difference > 0:
                self.climb_descent_sign = "^"
                self.altitude += step
            else:
                self.climb_descent_sign = "v"
                self.altitude -= step
        difference = self.targets["Speed"] - self.speed
        step = delta_time if self.targets["Status"] != "Landed" else 2 * delta_time
        if abs(difference) <= step:
            self.speed = self.targets["Speed"]
        else:
            self.speed += step * (1 if difference > 0 else -1)
        difference = (target_heading - self.heading + 180) % 360 - 180
        step = (2 * delta_time) if self.targets["Status"] != "Hold" else (
                4 * delta_time) if not self.before_hold_wpt else (
                2 * delta_time)
        if abs(difference) <= step:
            self.heading = target_heading
        else:
            self.heading += step * (1 if difference > 0 else -1)
        self.heading %= 360
        # Update: x_pos, y_pos
        speed_px_per_sec = self.speed * 20 / 3600
        rad = math.radians(self.heading)
        dx = math.sin(rad)
        dy = -math.cos(rad)
        dx *= speed_px_per_sec
        dy *= speed_px_per_sec
        self.x_pos += delta_time * dx
        self.y_pos += delta_time * dy
        if self.near_col:
            self.score_timer += delta_time
            while self.score_timer >= 15:
                score_change -= 40
                self.score_timer -= 15
        else:
            self.score_timer = 0
        return score_change


class Waypoint:
    def __init__(self, x_pos, y_pos, type, name: str, textures_dict: dict):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        self.name = name
        texture = textures_dict[type]
        self.surface = pygame.Surface((30, 20), pygame.SRCALPHA)
        self.texture = pygame.image.load(texture).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (10, 10))
        self.surface.blit(self.texture, (0, 10))
        text_surface = font.render(
            self.name,
            True,
            (255, 255, 255))
        self.surface.blit(text_surface, (30 - text_surface.get_width(), 0))


class Runway:
    def __init__(self, x_pos, y_pos, runways: list[str], texture: str = "runway.png"):
        if int(runways[0][:2]) > int(runways[1][:2]):
            runway_1 = runways[1]
            runway_2 = runways[0]
            runways = [runway_1, runway_2]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.runways = runways
        self.surface = pygame.Surface((90, 10), pygame.SRCALPHA)
        runway_heading = int(runways[0][:2]) * 10
        pygame_angle = -(runway_heading - 90)
        self.texture = pygame.image.load(texture).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (50, 9))
        self.surface.blit(self.texture, (20, 0))
        runway_1_text_surface = font.render(
            self.runways[0],
            True,
            (255, 255, 255))
        runway_2_text_surface = font.render(
            self.runways[1],
            True,
            (255, 255, 255))
        self.surface.blit(runway_1_text_surface, (0, 0))
        self.surface.blit(runway_2_text_surface, (90 - runway_2_text_surface.get_width(), 0))
        self.surface = pygame.transform.rotate(self.surface, pygame_angle)
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))
        runway_length = 44  # Change if the RUNWAY texture dimensions change (also keep in mind not to make the texture at the very end)
        half_length = runway_length / 2
        heading_rad = math.radians(runway_heading)
        dx = math.sin(heading_rad) * half_length
        dy = -math.cos(heading_rad) * half_length
        threshold_1 = (
            self.x_pos - dx - 5,
            self.y_pos - dy - 45
        )
        threshold_2 = (
            self.x_pos + dx - 5,
            self.y_pos + dy - 45
        )
        """
        Reason for above '-5' and '-45' is the airplane texture and surface, the surface is 50x50 px,
        and the texture is 10x10 px, so to get to the middle of the airplane TEXTURE, we need to go
        to coords (45, 5) of the airplane SURFACE.
        """
        self.runway_coords = [threshold_1, threshold_2]


class DistanceWarner:
    def check(self, airplane_list):
        # NOTE: Checks twice per pair, slight inefficiency, can be fixed later, not a bug though
        game_over = False
        for airplane in airplane_list:
            airplane.near_col = False
        for airplane in airplane_list:
            for airplane2 in airplane_list:
                if airplane is airplane2:
                    continue
                dist_diff = 50 if not (
                        airplane.targets["Status"].startswith("Lnd") or airplane2.targets["Status"].startswith(
                    "Lnd")) else 25 if not airplane.targets["Status"] == airplane2.targets["Status"] else 40
                alt_diff = 1000 if not (
                        airplane.targets["Status"].startswith("Lnd") or airplane2.targets["Status"].startswith(
                    "Lnd")) else 200 if not airplane.targets["Status"] == airplane2.targets["Status"] else 300
                dist = math.hypot(airplane.x_pos - airplane2.x_pos, airplane.y_pos - airplane2.y_pos)
                altitude_diff = abs(airplane.altitude - airplane2.altitude)
                if dist < dist_diff and altitude_diff < alt_diff:
                    airplane.near_col, airplane2.near_col = True, True
                if dist < 10 and altitude_diff < 70:
                    game_over = True
        return game_over


class AirplaneSpawner:
    def __init__(self, cooldown_s, max_airplanes, performance_mode):
        self.cooldown_s, self.max_airplanes = cooldown_s, max_airplanes
        self.callsigns = ["ETD", "UAE", "MEA", "QTR", "ETD", "ETD", "UAE", "UAE", "UAE", "UAE", "THY"]
        self.positions = [
            [450, 800, 250, 350, 4000, 2000],
            [100, 800, 250, 0, 5000, 2000],
            [50, 500, 250, 90, 7000, 2000],
            [50, 50, 250, 130, 4000, 2000],
            [450, 50, 250, 180, 8000, 2000],
            [800, 450, 250, 300, 3000, 2000]
        ]
        self.last_pos = []
        self.performance_mode = performance_mode

    def new_plane(self):
        retrying = True
        while retrying:
            position = choice(self.positions)
            if self.last_pos != position:
                retrying = False
        self.last_pos = position
        num = randint(1, 9999)
        num = str(num) if num >= 1000 else f"{num:03d}"
        callsign = f"{choice(self.callsigns)}{num}"
        if self.performance_mode == "HIGH":
            return Airplane(callsign, position[0], position[1], position[2], position[3], position[4], position[5],
                            "texture1.png")
        else:
            return Airplane(callsign, position[0], position[1], position[2], position[3], position[4], position[5],
                            "texture1.png", max_trail_length=2)
