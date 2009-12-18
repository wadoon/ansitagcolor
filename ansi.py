#/usr/bin/python 

import sys
from pyparsing import *

# program info
__author__ = "Alexander Weigl <alex953@gmail.com>"
__version__= "0.0.1"
__date__   = "25. Jul. 2006"

# variables

ansi_colors = {
    'Reset'  :9,
    'Black'  :0,
    'Red'    :1,
    'Green'  :2,
    'Yellow' :3,
    'Blue'   :4,
    'Magenta':5,
    'Cyan'   :6,
    'White'  :7  
    }

#Build a mapping betwenn user and color
abbr_color_name = {}
for name in ansi_colors.keys():
    letter = name[0]
    abbr_color_name[letter.lower()]= name
    abbr_color_name[name]= name
    abbr_color_name[letter.upper()]= name

abbr_color_name['rs']='Reset'


# other values
ansi_reset           = 0   #Reset / Normal  all attributes off
ansi_bold            = 1   #Intensity: Bold	
ansi_faint           = 2   #Intensity: Faint
ansi_italic          = 3   #Italic: on  
ansi_underline       = 4   #Underline: Single
ansi_blink_slow      = 5   #Blink: Slow less than 150 per minute
ansi_blink_rapid     = 6   #Blink: Rapid	
ansi_switch_color    = 7   #Image: Negative	inverse or reverse; swap foreground and background
ansi_conceal         = 8   #Conceal	
ansi_twice_underline = 21  #Underline: Double	
ansi_intensity_normal= 22  #Intensity: Normal
ansi_no_underline    = 24  #Underline: None	
ansi_blink_off       = 25  #Blink: off	
ansi_switch_color_off= 27  #Image: Positive	
ansi_reveal          = 28  #Conceal: Off

_normal_color       = (30,40)   #Addition to color
_intensity_color    = (90,100)  #Addition to color

CSI = "\033["

class style(object):
    def __init__(self,*args):
        self.args = set(args)

    def __copy(self):
        return style(*self.args)

    def __str__(self):
        return CSI+';'.join(str(x) for x in  self.args)+'m'

    def __iadd__(self,other):
        for o in iter(other):
            self.args.add(o)
        return self

    def __isub__(self,other):
        for o in iter(other):
            self.args.remove(o)
        return self
    
    def __iand__(self,other):
        if type(other) is set:
            self.args &= other
        elif type(other) is style:
            self.args &= style.args
        return self

    def __add__(self,other):
        copy = self.__copy() 
        copy += other
        return copy

    def __sub__(self,other):
        copy =  self.__copy() 
        copy -= other
        return copy
    
    def __and__(self,other):
        copy =  self.__copy() 
        copy &= other
        return copy
    

    def __iter__(self):
        return iter(self.args)
        

class AnsiTerminal:
    """
    A AnsiTerminal is a wrapper above a handle for writing ansi sequences to terminals.
    With the attribute @enabled@ you can block all ansi sequences for printout
    """            
    def __init__(self,handle=sys.stdout, enabled = True):
        """
        Create a new AnsiTerminal for the file/console handle. 
        The default is enable true and the handle is sys.stdout
        """

        self.output = handle
        self.set_color = self.set_normal_color  
        self.enabled = enabled # and handle.isatty(): 

    def __lshift__(self, obj):
        self.output.write(obj)
        
    def set_raw(self, *args):
        """
        writes all *args as styled commands 'm' to the handle
        """
        if not self.enabled: return
        args = map( lambda x: str(x), [x for x in args if x is not None] )
        self._write_raw( ';'.join(args) + 'm' )

    def _write_raw(self, suffix):
        """
        writes a the suffix prefixed by the CSI to the handle
        """
        if not self.enabled: return

        self.output.write(CSI)
        self.output.write(suffix)

    def set_blink(self, cmd='off'):
        """
        sets the blinking of the text in the terminal
        values for cmd: 'off' , ('on','slow), 'rapid'
 
        """
        cmd = cmd.lower()
        if cmd == 'on' or cmd == 'slow':
            blink = ansi_blink_slow
        elif cmd == 'rapid':
            blink = ansi_blink_rapid
        else:
            blink = ansi_blink_off
        self.set_raw(blink)

    def set_bold(self, cmd='off'):
        """
        sets a bold font
        values for cmd: 'on', 'off'
        """
        cmd = cmd.lower()
        if cmd == 'off':
            self.set_raw(ansi_intensity_normal)
        else:
            self.set_raw(ansi_bold)
            
    def set_underline(self, cmd='off'):
        """
        sets the underlining of the text
        values for cmd: ('on','single'), 'double' , 'off'
        """
        cmd = cmd.lower()
        if cmd == 'on' or cmd == 'single':
            raw = ansi_underline
        elif cmd == 'double':
            raw =ansi_twice_underline
        else:
            raw = ansi_no_underline
        self.set_raw(raw)

    def set_normal_color(self, fg,bg):
        """
        setting the terminal color using the _normal_color (30,40)
        """
        self.__set_color(fg,bg)

    def set_intensity_color(self, fg,bg):
        """
        setting the terminal color using the _intensity_color (90,100)
        """
        self.__set_color(fg,bg,_intensity_color)

    def __get_color(self, name):
        return ansi_colors[ abbr_color_name[ name ] ]
            
    def __set_color(self, fg, bg, cscheme=_normal_color ):
        fg_v = None if fg is None else self.__get_color(fg) + cscheme[0]
        bg_v = None if bg is None else self.__get_color(bg) + cscheme[1]
        self.set_raw(fg_v,bg_v)
            
    def reset(self):
        self.set_raw(ansi_reset)

    def scroll_page_up(self, page=1):
        """
        Command: CSI n S
        Name:    SU 
        Scroll whole page up by n (default 1) lines. New lines are added at the bottom. (not ANSI.SYS)
        """
        self._write_raw( page + 'S' )
    
    def scroll_page_down(self, page=1):
        """
        Command: CSI n T 
        Name:    SD
        Scroll whole page down by n (default 1) lines. New lines are added at the top. (not ANSI.SYS)
        """
        self._write_raw(  page + 'T' )
    
    def clear_screen(self,type=2):
        """
        Command: CSI n J
        Name; ED
        Clears part of the screen. If n is zero (or missing), clear from cursor to end of screen. If n is one, clear from cursor to beginning of the screen. If n is two, clear entire screen (and moves cursor to upper left on MS-DOS ANSI.SYS).
        """
        self._write_raw( type  + 'J' )

    def save_cursor(self):
        self._write_raw( 's' )
        
    def restore_cursor(self):
        self._write_raw( 'u' )
    
    def moveto(self, row,col):
        self._write_raw( row + ';' +col + 'f') 

    def _parse(self, command):
        #print '__parse: ' , command
        command = statement.parseString(command)[1:-1]
        #print command
        if command[0] == '+' or command[0] == '-':
            self.__set_switch(state=command[0], switch = command[1] )
        else:
            argument = command[0]
            values = []
            for v in range(2, len( command  ) ,2):
                values += (command[v],)
            self.__set_argument(argument,values)
        
    def __set_argument(self, arg,values):
        #print arg, '->', values
        if arg == 'c':
            self.set_color(values[0],values[1])
        elif arg == 'm':
            self.moveto(values[0],values[1])
        elif arg=='r':
            self.reset()
        else:
            if __debug__:
                self.output.write(  '<E: not well known switch: %s>' % arg )

    def __set_switch(self, switch,state):
        state = 'on' if state=='+' else 'off'
        if switch == 'b':
            self.set_blink(state)
        elif switch =='u':
            self.set_underline(state)
        else:
            if __debug__:
                self.output.write( '<E: not well known switch: %s>' % switch )

#input parsing
__grammar = """
 # root
   statement :== '[' innerStatement  ']'
   innerStatement :==   single_stmt 
                      | param_stmt
                      | onoff_stmt;
   
   single_stmt :== 'r'; #only reset
   param_stmt  :== 'c:' integer ',' integer; # nur color
   onoff_stmt  :== 'b'|'u' '+'|'-'
 #ziffern:
   integer :== '' | 0..9;
"""

letter = Or( Word(alphas+nums,max=10) | Literal('_').setParseAction( 
        lambda s,p,t: [ None ]
) ) 

arglist = letter + ZeroOrMore( Literal(',') + letter)
params_cmd = letter + Optional( Literal(':') + arglist )

switch_cmd = Or(Literal('+') |'-' )
onoff_cmd  = switch_cmd + letter 

inner_stmt = Or(onoff_cmd| params_cmd)
statement = Literal('[') + inner_stmt + Literal(']')

onoff_cmd.setResultsName('on_off')
params_cmd.setResultsName('param')

__printing__ = True

stdout = AnsiTerminal(sys.stdout)
stderr = AnsiTerminal(sys.stderr)


def output(text,terminal=stdout, auto_reset=False):    
    while len(text) > 0:
        start,end = text.find('['), text.find(']')

        #no more tags to translated, you can print the rest
        if start == -1 or end == -1:
            print text
            break

        printable = text[0:start]
        command = text[start:end+1]
        text = text[end+1:]
        
        print printable,
        del printable
        
        if __printing__: terminal._parse(command)
    if auto_reset:
        terminal.reset()


if __name__=='__main__':
    try:
        import psyco
        psyco.log()
        psyco.full()
        psyco.profile()
    except ImportError:
        pass
    import sys        
    output(  ' '.join(sys.argv[1:])  );


