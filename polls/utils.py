class ProgressBar(object):
    def __init__(self, title, maximum, value):
        self.title = title
        self.maximum = maximum
        self.value = value

        if self.maximum == 0:
            self.maximum = 1

    def __repr__(self):
        output = '<div class="progress">%s</div>'
        output = output % '<div class="bar" style="width:%s%%;"></div>'
        return output % ( self.value * 100 / self.maximum )
