NE, ENE, ESE, SE, SSE, S, SW, WSW, WNW, NW, NNW, N, NNE = range(13)

# slide 13 of http://www.cs.uu.nl/docs/vakken/gd/steven2.pdf
placements = {NE: 0.000, ENE: 0.070, ESE: 0.100, SE: 0.175, SSE: 0.200,
              S: 0.900, SW: 0.600, WSW: 0.500, WNW: 0.470, NW: 0.400,
              NNW: 0.575, N: 0.800, NNE: 0.150}

class Place:

    def __init__(self, name, font, location, position, radius):
        self.name = name
        self.font = font
        self.location = location
        self.position = position
    
        self.placement = NE
        self.radius = radius
        self.buffer = 2

    def __repr__(self):
        return '<Place: %s>' % self.name
    
    def __hash__(self):
        return id(self)
    
    def _update_label_shape(self):
        """
        """
        x, y = self.position.x, self.position.y
        
        if self.placement in (NE, ENE, ESE, SE):
            x += self.radius + self._width/2
        
        if self.placement in (NW, WNW, WSW, SW):
            x -= self.radius + self._width/2

        if self.placement in (NW, NE):
            y -= self._height/2

        if self.placement in (SW, SE):
            y += self._height/2

        if self.placement in (ENE, WNW):
            y -= self._height/6

        if self.placement in (ESE, WSW):
            y += self._height/6
        
        if self.placement in (NNE, SSE, NNW):
            _x = self.radius * cos(pi/4) + self._width/2
            _y = self.radius * sin(pi/4) + self._height/2
            
            if self.placement in (NNE, SSE):
                x += _x
            else:
                x -= _x
            
            if self.placement in (SSE, ):
                y += _y
            else:
                y -= _y
        
        if self.placement == N:
            y -= self.radius + self._height / 2
        
        if self.placement == S:
            y += self.radius + self._height / 2
        
        x1, y1 = x - self._width/2, y - self._height/2
        x2, y2 = x + self._width/2, y + self._height/2
        
        self._label_shape = Polygon(((x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)))
    
    def move(self):
        self.placement = choice(placements.keys())
        self._update_label_shape()
    
    def placement_energy(self):
        return placements[self.placement]
    
    def overlap_energy(self, other):
        if self.overlaps(other):
            return min(10.0 / self.rank, 10.0 / other.rank)

        return 0.0
    
    def overlaps(self, other, reflexive=True):
        overlaps = self.mask_shape().intersects(other.label_bbox())
        
        if reflexive:
            overlaps |= other.overlaps(self, False)

        return overlaps

    def can_overlap(self, other, reflexive=True):
        range = self.radius + hypot(self._width + self.buffer*2, self._height + self.buffer*2)
        distance = hypot(self.position.x - other.position.x, self.position.y - other.position.y)
        can_overlap = distance <= range
        
        if reflexive:
            can_overlap |= other.can_overlap(self, False)

        return can_overlap
