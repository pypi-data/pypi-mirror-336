from pygeometry2d import XY, GeomUtils

from pytqs.drawning import TQSDrawning
from pytqs.elements import TQSBlock

from TQS.TQSDwg import Dwg

import math

class TQSAlvestDrawning(TQSDrawning):
    def __init__(self, drawning_path: str = None, dwg: Dwg = None, auto_update_entitys: bool = False, iterate_through_invisible_layers=True) -> None:
        super().__init__(drawning_path, dwg, auto_update_entitys, iterate_through_invisible_layers)
        self._blocks = None

    def _add_graute_lines(self, points: list[XY], n: int):
        self.draw.polyline(points, layer="213")
        bb = GeomUtils.get_min_max_point(points)
        mid_point = bb.mid

        if n % 2 == 1:
            line_pt1 = XY(mid_point.x, -4)
            line_pt2 = XY(mid_point.x, 4)
            self.draw.line(p1=line_pt1, p2=line_pt2, layer="213")

        for i in range(n // 2):
            offset = 0.25 if n % 2 == 0 else 0
            line_pt1 = XY(mid_point.x - 0.5 * (n // 2) + 0.5 * i + offset, -4)
            line_pt2 = XY(mid_point.x - 0.5 * (n // 2) + 0.5 * i + offset, 4)
            self.draw.line(p1=line_pt1, p2=line_pt2, layer="213")
            
            line_pt3 = XY(mid_point.x + 0.5 * (n // 2) - 0.5 * i - offset, -4)
            line_pt4 = XY(mid_point.x + 0.5 * (n // 2) - 0.5 * i - offset, 4)
            self.draw.line(p1=line_pt3, p2=line_pt4, layer="213")

        self.draw.circle(center=mid_point, diameter=1.0, layer="224")

    def create_grout_bar_definition(self):
        if not self.dwg.blockstable.IsDefined("$PFERV"):
            with self.draw.block_definition("$PFERV"):
                self.draw.polyline([XY(-0.35355339, 0.35355339), XY(-0.5, 0.0), XY(-0.35355339, -0.35355339), XY(0.0, -0.5), XY(0.35355339, -0.35355339), XY(0.5, 0.0), XY(0.35355339, 0.35355339), XY(0.0, 0.5), XY(-0.35355339, 0.35355339)], is_filled=True, layer = 0)
                self.draw.line(p1=XY(-0.55, 0), p2=XY(1.05, 0), layer = 0)
                self.draw.line(p1=XY(0, -0.55), p2=XY(0, 0.55), layer = 0)

        for diameter in [8, 10, 12.5, 16, 20]:
            if not self.dwg.blockstable.IsDefined(f"$PFERV_pf{diameter:.1f}"):
                with self.draw.block_definition(f"$PFERV_pf{diameter:.1f}"):
                    self.draw.block("$PFERV", XY.zero(), 0, diameter/10, diameter/10, layer=0)
                    self.draw.text(f"pf{diameter:.1f}", XY(0, 3), 5, 0, layer=198)

    def create_block_19(self, suffix: str = ""):
        block_name = f"P2015{suffix}"
        with self.draw.block_definition(block_name):
            external_points = [XY(-9.5, -7.0), XY(9.5, -7.0), XY(9.5, 7.0), XY(-9.5, 7.0), XY(-9.5, -7.0)]
            hole1_points = [XY(-7.0, -3.5), XY(-6.0, -4.5), XY(6.0, -4.5), XY(7.0, -3.5), XY(7.0, 3.5), XY(6.0, 4.5), XY(-6.0, 4.5), XY(-7.0, 3.5), XY(-7.0, -3.5)]
            
            self.draw.polyline(external_points, layer="0")
            self.draw.polyline(hole1_points, layer="203")
            
            if suffix == "G":
                self._add_graute_lines(hole1_points, 27)

    def create_block_34(self, suffix: str = ""):
        block_name = f"P3515{suffix}"
        with self.draw.block_definition(block_name):
            external_points = [XY(-17.0, -7.0), XY(17.0, -7.0), XY(17.0, 7.0), XY(-17.0, 7.0), XY(-17.0, -7.0)]
            hole1_points = [XY(-14.5, -3.5), XY(-13.5, -4.5), XY(-4.75, -4.5), XY(-3.75, -3.5), XY(-3.75, 3.5), XY(-4.75, 4.5), XY(-13.5, 4.5), XY(-14.5, 3.5), XY(-14.5, -3.5)]
            hole2_points = [XY(-1.25, -3.5), XY(-0.25, -4.5), XY(13.5, -4.5), XY(14.5, -3.5), XY(14.5, 3.5), XY(13.5, 4.5), XY(-0.25, 4.5), XY(-1.25, 3.5), XY(-1.25, -3.5)]
            
            self.draw.polyline(external_points, layer="0")
            self.draw.polyline(hole1_points, layer="203")
            self.draw.polyline(hole2_points, layer="203")
            
            if suffix == "G1":
                self._add_graute_lines(hole2_points, 30)
            elif suffix == "G2":
                self._add_graute_lines(hole1_points, 20)
            elif suffix == "F":
                self._add_graute_lines(hole1_points, 20)
                self._add_graute_lines(hole2_points, 30)

    def create_block_39(self, suffix: str = ""):
        block_name = f"P4015{suffix}"
        with self.draw.block_definition(block_name):
            external_points = [XY(-19.5, -7), XY(19.5, -7), XY(19.5, 7), XY(-19.5, 7), XY(-19.5, -7)]
            hole1_points = [XY(-17.0, -3.5), XY(-16.0, -4.5), XY(-2.25, -4.5), XY(-1.25, -3.5), XY(-1.25, 3.5), XY(-2.25, 4.5), XY(-16.0, 4.5), XY(-17.0, 3.5), XY(-17.0, -3.5)]
            hole2_points = [XY(1.25, -3.5), XY(2.25, -4.5), XY(16.0, -4.5), XY(17.0, -3.5), XY(17.0, 3.5), XY(16.0, 4.5), XY(2.25, 4.5), XY(1.25, 3.5), XY(1.25, -3.5)]
            
            self.draw.polyline(external_points, layer="0")
            self.draw.polyline(hole1_points, layer="203")
            self.draw.polyline(hole2_points, layer="203")
            
            if suffix == "G":
                self._add_graute_lines(hole2_points, 30)
            elif suffix == "F":
                self._add_graute_lines(hole1_points, 30)
                self._add_graute_lines(hole2_points, 30)

    def create_block_54(self, suffix: str = ""):
        block_name = f"P5515{suffix}"
        with self.draw.block_definition(block_name):
            external_points = [XY(-27.0, -7.0), XY(27.0, -7.0), XY(27.0, 7.0), XY(-27.0, 7.0), XY(-27.0, -7.0)]
            hole1_points = [XY(-24.5, -3.5), XY(-23.5, -4.5), XY(-9.75, -4.5), XY(-8.75, -3.5), XY(-8.75, 3.5), XY(-9.75, 4.5), XY(-23.5, 4.5), XY(-24.5, 3.5), XY(-24.5, -3.5)]
            hole2_points = [XY(-6.25, -3.5), XY(-5.25, -4.5), XY(5.25, -4.5), XY(6.25, -3.5), XY(6.25, 3.5), XY(5.25, 4.5), XY(-5.25, 4.5), XY(-6.25, 3.5), XY(-6.25, -3.5)]
            hole3_points = [XY(8.75, -3.5), XY(9.75, -4.5), XY(23.5, -4.5), XY(24.5, -3.5), XY(24.5, 3.5), XY(23.5, 4.5), XY(9.75, 4.5), XY(8.75, 3.5), XY(8.75, -3.5)]
            
            self.draw.polyline(external_points, layer="0")
            self.draw.polyline(hole1_points, layer="203")
            self.draw.polyline(hole2_points, layer="203")
            self.draw.polyline(hole3_points, layer="203")
            
            if suffix == "G1":
                self._add_graute_lines(hole2_points, 24)
            elif suffix == "G1_2":
                self._add_graute_lines(hole3_points, 30)
            elif suffix == "G2":
                self._add_graute_lines(hole2_points, 24)
                self._add_graute_lines(hole3_points, 30)
            elif suffix == "G2_2":
                self._add_graute_lines(hole1_points, 30)
                self._add_graute_lines(hole3_points, 30)
            elif suffix == "F":
                self._add_graute_lines(hole1_points, 30)
                self._add_graute_lines(hole2_points, 24)
                self._add_graute_lines(hole3_points, 30)

    def create_block_14(self, suffix: str = ""):
        block_name = f"P1515{suffix}"
        with self.draw.block_definition(block_name):
            external_points = [XY(-7.0, -7.0), XY(7.0, -7.0), XY(7.0, 7.0), XY(-7.0, 7.0), XY(-7.0, -7.0)]
            hole1_points = [XY(-4.5, -3.5), XY(-3.5, -4.5), XY(3.5, -4.5), XY(4.5, -3.5), XY(4.5, 3.5), XY(3.5, 4.5), XY(-3.5, 4.5), XY(-4.5, 3.5), XY(-4.5, -3.5)]
            
            self.draw.polyline(external_points, layer="0")
            self.draw.polyline(hole1_points, layer="203")
            
            if suffix == "G":
                self._add_graute_lines(hole1_points, 17)

    def create_block_29(self, suffix: str = ""):
        block_name = f"P3015{suffix}"
        with self.draw.block_definition(block_name):
            external_points = [XY(-14.5, -7), XY(14.5, -7), XY(14.5, 7), XY(-14.5, 7), XY(-14.5, -7)]
            hole1_points = [XY(-12.0, -3.5), XY(-11.0, -4.5), XY(-2.25, -4.5), XY(-1.25, -3.5), XY(-1.25, 3.5), XY(-2.25, 4.5), XY(-11.0, 4.5), XY(-12.0, 3.5), XY(-12.0, -3.5)]
            hole2_points = [XY(1.25, -3.5), XY(2.25, -4.5), XY(11.0, -4.5), XY(12.0, -3.5), XY(12.0, 3.5), XY(11.0, 4.5), XY(2.25, 4.5), XY(1.25, 3.5), XY(1.25, -3.5)]
            
            self.draw.polyline(external_points, layer="0")
            self.draw.polyline(hole1_points, layer="203")
            self.draw.polyline(hole2_points, layer="203")
            
            if suffix == "G":
                self._add_graute_lines(hole2_points, 20)
            elif suffix == "F":
                self._add_graute_lines(hole1_points, 20)
                self._add_graute_lines(hole2_points, 20)

    def create_block_44(self, suffix: str = ""):
        block_name = f"P4515{suffix}"
        with self.draw.block_definition(block_name):
            external_points = [XY(-22.0, -7.0), XY(22.0, -7.0), XY(22.0, 7.0), XY(-22.0, 7.0), XY(-22.0, -7.0)]
            hole1_points = [XY(-19.5, -3.5), XY(-18.5, -4.5), XY(-8.5, -4.5), XY(-7.5, -3.5), XY(-7.5, 3.5), XY(-8.5, 4.5), XY(-18.5, 4.5), XY(-19.5, 3.5), XY(-19.5, -3.5)]
            hole2_points = [XY(-5, -3.5), XY(-4, -4.5), XY(4, -4.5), XY(5, -3.5), XY(5, 3.5), XY(4, 4.5), XY(-4, 4.5), XY(-5, 3.5), XY(-5, -3.5)]
            hole3_points = [XY(7.5, -3.5), XY(8.5, -4.5), XY(18.5, -4.5), XY(19.5, -3.5), XY(19.5, 3.5), XY(18.5, 4.5), XY(8.5, 4.5), XY(7.5, 3.5), XY(7.5, -3.5)]
            
            self.draw.polyline(external_points, layer="0")
            self.draw.polyline(hole1_points, layer="203")
            self.draw.polyline(hole2_points, layer="203")
            self.draw.polyline(hole3_points, layer="203")
            
            if suffix == "G1":
                self._add_graute_lines(hole2_points, 19)
            elif suffix == "G1_2":
                self._add_graute_lines(hole3_points, 23)
            elif suffix == "G2":
                self._add_graute_lines(hole2_points, 19)
                self._add_graute_lines(hole3_points, 23)
            elif suffix == "G2_2":
                self._add_graute_lines(hole1_points, 23)
                self._add_graute_lines(hole3_points, 23)
            elif suffix == "F":
                self._add_graute_lines(hole1_points, 23)
                self._add_graute_lines(hole2_points, 19)
                self._add_graute_lines(hole3_points, 23)

    def set_alvest_blocks_definition_m15(self):
        self.create_block_14()
        self.create_block_14("G")
        
        self.create_block_29()
        self.create_block_29("G")
        self.create_block_29("F")
        
        self.create_block_44()
        self.create_block_44("G1")
        self.create_block_44("G1_2")
        self.create_block_44("G2")
        self.create_block_44("G2_2")
        self.create_block_44("F")
    
    def set_alvest_blocks_definition_m20(self):
        self.create_block_19()
        self.create_block_19("G")
        
        self.create_block_34()
        self.create_block_34("G1")
        self.create_block_34("G2")
        self.create_block_34("F")
        
        self.create_block_39()
        self.create_block_39("G")
        self.create_block_39("F")
        
        self.create_block_54()
        self.create_block_54("G1")
        self.create_block_54("G1_2")
        self.create_block_54("G2")
        self.create_block_54("G2_2")
        self.create_block_54("F")
        

    def _replace_block(self, old_block: TQSBlock, new_block_name: str, modified_angle: float = None):
        self.delete(old_block)
        new_block = self.draw.block(new_block_name, old_block.point, modified_angle or old_block.angle, old_block.scale_x, old_block.scale_y, layer=old_block.layer)
        if self._blocks and new_block:
            self._blocks.append(new_block)
            self._blocks.remove(old_block)

    def remove_all_grouts(self):
        blocks = self._elements.filter_type(TQSBlock).filter_layer([241, 245]) if self._elements else self.quick_filter(types=[TQSBlock], layers=[161, 241, 245])
        for block in blocks[:]:
            if "G" in block.block_name or  block.block_name[-1] == "F":
                self._replace_block(block, block.block_name.partition("G")[0].partition("F")[0])
            elif "$PFERV_pf" in block.block_name:
                self.delete(block)

    def grout_by_point(self, point: XY, diameter: int|str, ignored_diameter: float = 10) -> bool:
        if not self._blocks:
            self._blocks = self.elements.filter_type(TQSBlock).filter_layer([241, 245])

        possible_blocks = [blk for blk in self._blocks if blk.point.distance(point) < 27]
        block = [(blk, pl) for blk in possible_blocks for pl in blk.elements.filter_layer(203) if pl.is_point_inside(point)]

        if not block:
            print(f"ERRO AO GRAUTEAR PONTO {point}")
            return False

        block, pl = (block[0][0], block[0][1])

        with self.auto_update_entitys_temporarily():
            index = block.elements.filter_layer(203).index(pl)
            stats = False
            if block.block_name == "P2015":
                self._replace_block(block, "P2015G") 
                stats = True
            elif block.block_name == "P4015":
                if index == 0:
                    self._replace_block(block, "P4015G", block.angle+math.pi) 
                    stats = True
                elif index == 1:
                    self._replace_block(block, "P4015G") 
                    stats = True
            elif block.block_name == "P4015G":
                if index == 0:
                    self._replace_block(block, "P4015F") 
                    stats = True
            elif block.block_name == "P3515":
                if index == 0:
                    self._replace_block(block, "P3515G2")
                    stats = True
                elif index == 1:
                    self._replace_block(block, "P3515G1")
                    stats = True
            elif block.block_name == "P3515G1":
                if index == 0:
                    self._replace_block(block, "P3515F")
                    stats = True
            elif block.block_name == "P3515G2":
                if index == 1:
                    self._replace_block(block, "P3515F")
                    stats = True
            elif block.block_name == "P5515":
                if index == 0:
                    self._replace_block(block, "P5515G1_2", block.angle+math.pi)
                elif index == 1:
                    self._replace_block(block, "P5515G1")
                else:
                    self._replace_block(block, "P5515G1_2")
                stats = True
            elif block.block_name == "P5515G1":
                if index == 0:
                    self._replace_block(block, "P5515G2", block.angle+math.pi)
                    stats = True
                elif index == 2:
                    self._replace_block(block, "P5515G2")
                    stats = True
            elif block.block_name == "P5515G1_2":
                if index == 0:
                    self._replace_block(block, "P5515G2_2")
                    stats = True
                elif index == 1:
                    self._replace_block(block, "P5515G2")
                    stats = True
            elif block.block_name == "P5515G2":
                if index == 0:
                    self._replace_block(block, "P5515F")
                    stats = True
            elif block.block_name == "P5515G2_2":
                if index == 1:
                    self._replace_block(block, "P5515F")
                    stats = True

        if diameter not in [ignored_diameter, 0]:
            if isinstance(diameter, str) and "2x" in diameter:
                diameter = int(diameter[2:])
                if diameter == 12:
                    diameter = 12.5
                self.draw.block(f"$PFERV_pf{diameter:.1f}", pl.center()+XY(0,2), 0, 1, 1, layer = 161)
                self.draw.block(f"$PFERV_pf{diameter:.1f}", pl.center()-XY(0,2), 0, 1, 1, layer = 161)
            else:
                if diameter == 12:
                    diameter = 12.5
                self.draw.block(f"$PFERV_pf{diameter:.1f}", pl.center(), 0, 1, 1, layer = 161)
        return stats


if __name__ == "__main__":
    model_path = "C:\\TQS\\000-Modelo-Alvenaria-R04\\Térreo\\Térreo.DWG"
    drawning = TQSAlvestDrawning(model_path, iterate_through_invisible_layers=False)
    #print(any(block for block in drawning.defined_blocks if block in ['P2015', 'P3515', 'P4015', 'P5515']))
    drawning.set_layer_state([161, 198, 203, 241, 245], True)
    drawning.create_grout_bar_definition()
    drawning.set_alvest_blocks_definition_m15()
    drawning.set_alvest_blocks_definition_m20()
    drawning.save()