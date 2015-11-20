#!/usr/local/bin/perl
# HTML2RTF  --  Make an RTF rendering of an HTML file.
#
$html2rtf_version = 'HTML2RTF v1.1a';   # by sean@qrd.org
$html2rtf_revision = 
    ' Time-stamp: <1997-11-25 22:25:30 MST sburke@babel.ling.nwu.edu> ';
# This package is Copyright 1996- by Sean M. Burke, sean@qrd.org
#
# See the docs at http://www.ling.nwu.edu/~sburke/html2rtf/
#  Quick usage summary:    html2rtf.pl input.html
#
# html2rtf is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any
# later version.
#
# html2rtf is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# To see a copy of the GNU General Public License, see
# http://www.ling.nwu.edu/~sburke/gnu_release.html, or write to the
# Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# ------------------------------------------------------------

## Configurables follow...
$debug = 1;
 # 0 makes this program totally quiet except for errors or warnings
 #    -- good for use, say, in a batch file
 # 1 makes this program say friendly things like say what file
 #    it's working on.
 # above 1 makes it spit out the RTF code on STDOUT as well as to a file.


# Here set the name of the fonts to use for proportional (normal)
# and monospace (CODE, PRE) text.  They have to be the exact (?) name
# of the fonts as they exist on your system.
$proportional_font = 'Times New Roman';
  # Alternately, choose, say, 'Arial', or maybe 'Optima' or a Schoolbook.
  # Superpimps use 'DomCasual BT' or 'Cooper Blk BT'
$monospace_font = 'Courier New';

# These determine what characters styles
# are rendered as what font attributes.
@italic_styles = ('I', 'CITE', 'VAR');
@bold_styles = ('STRONG', 'B', 'DEFN');
@underline_styles = ('U', 'EM');

$tab = 720; # distance between tab stops, in twips.  720 twips = .5 inches.

# How to render horizontal rules
$hr_style = '\qc\emdash\emdash\emdash';

# for a fancier and larger HR, use '\qc{\fs100\b ~}'
# Wishlist: write logic that'll spit out different /kinds/ of HRs
#  depending on the indent level?

$paragraph_space_before = 90;
  # Each <P> is preceded by this many twips of space downward
  # twip == 1/1440th of an inch == 1/20th of a point
  #  (Cf. point = 1/72nd of an inch)
$heading_space_before = $paragraph_space_before * 2;
  # Each heading style (H1-H6) is preceded by this many
  # twips of space downward.

@heading_styles = ( '\fs55 ', '\fs50 ', '\fs45 ',
		'\fs40 ', '\fs35 ', '\fs30 ');
	# Styles for the headings, starting from H1, ending with H6
	# \\fs40 means 20-point, \\fs50 means 25-point, etc.

#What follows is the association of the contents of ampersand entities
# to what they expand do.  I've quoted all 8-bit values here just so
# the PERL scripts doesn't get manged in transit.
# You can add anything you want here.

%entities = split(/[ \n]*,[ \n]*/,
"szlig,\xdf,eth,\xf0,ETH,\xd0,thorn,\xfe,THORN,\xde,yuml,\xff,
yacute,\xfd,Yacute,\xdd,uuml,\xfc,Uuml,\xdc,ugrave,\xf9,
Ugrave,\xd9,ucirc,\xfb,Ucirc,\xdb,uacute,\xfa,Uacute,\xda,
ocirc,\xf4,Ocirc,\xd4,
otilde,\xf5,Otilde,\xd5,oslash,\xf8,Oslash,\xd8,ograve,\xf2,
Ograve,\xd2,oacute,\xf3,Oacute,\xd3,ntilde,\xf1,Ntilde,\xd1,
iuml,\xef,Iuml,\xcf,igrave,\xec,Igrave,\xcc,icirc,\xee,
Icirc,\xce,iacute,\xed,Iacute,\xcd,euml,\xeb,Euml,\xcb,
egrave,\xe8,Egrave,\xc8,ecirc,\xea,Ecirc,\xca,eacute,\xe9,
Eacute,\xc9,ccedil,\xe7,Ccedil,\xc7,aelig,\xe6,AElig,\xc6,
atilde,\xe3,Atilde,\xc3,agrave,\xe0,Agrave,\xc0,acirc,\xe2,
Acirc,\xc2,aacute,\xe1,Aacute,\xc1,ouml,\xf6,Ouml,\xd6,aring,\xe5,
Aring,\xc5,auml,\xe4,Auml,\xc4,quot,\",amp,\&,gt,\>,lt,\<,
copy,\xa9,reg,\xae,
ensp,\\enspace ,emsp,\\emspace ,nbsp,\\~,\#92,\\\\,\#123,\\\{,\#125,\\\},
\#13,\\par,\#10,\\par,\#013,\\par,\#010,\\par" );
  # Those last two lines are RTF-specific.  Everything before is reusable
  # in non-RTF things.


######################################################################
## END of constants & configurables.
## Don't change anything from here on, unless you really know
##  what you're doing.
######################################################################

$charset = '\fcharset255';
  # 255 = OEM, supposedly a good approximation of ISO-Latin-1

$paragraph_space_before = "\\sb$paragraph_space_before";
$heading_space_before = "\\sb$heading_space_before";

$fonttable = "\\deff0 {\\fonttbl
{\\f0\\froman $charset $proportional_font;}
{\\f1\\fmodern $charset $monospace_font;}}";

# You can add additional fonts to the font table there if you want
# to use them, for headings, say.
# E.g., to add Arial as a third font and to have headings in it, go:
#   $fonttable = "\\deff0 {\\fonttbl
#   {\\f0\\froman $charset $proportional_font;}
#   {\\f1\\fmodern $charset $monospace_font;}}";
#   {\\f2\\fswiss $charset Arial;}}";
#
# Then to change the heading styles to Arial bold italic:
#   @heading_styles = ( '\fs55\f2\b\i ', '\fs50\f2\b\i ', '\fs45\f2\b\i ',
#   		'\fs40\f2\b\i ', '\fs35\f2\b\i ', '\fs30\f2\b\i ');
#
# Don't forget $charset, or the character translation won't work.
#
# Note the font family names -- Arial's is "swiss".  SPECIFYING THE FAMILY
# NAME IS OPTIONAL.  See the RTF specs for the allowable family names.

$* = 1;  #don't assume each string is just one line long.

$init = "{\\rtf1\\ansi $fonttable
{\\colortbl\\red0\\green0\\blue0;}
{\\stylesheet{\\fs20 \\snext0 Normal;}}\n";

$underline_re = '(' . join('|', @underline_styles) . ')';
$italic_re = '(' . join('|', @italic_styles) . ')';
$bold_re = '(' . join('|', @bold_styles) . ')';
$close_re = '(' . join('|', @underline_styles,
		@italic_styles, @bold_styles) . ')';

######################################################################
$stamp = $html2rtf_version;
if ($html2rtf_revision =~ /\<([^\>]+)/) {
 $html2rtf_revision = $1;  # gussy it up.
 $html2rtf_revision =~ tr/ /_/;
 $stamp .= ' (revision ' . $html2rtf_revision . ')';
}

print "Starting $stamp\n" if ($debug > 0);

foreach $file (@ARGV) {
 # reset some states
 $pre_state = 0;
 undef @list_level;
 undef @list_type;

 die "Can't open input file $file" unless open(INFILE, $file);
 print "Converting $file\n" if ($debug > 0);
 $instream = join('', <INFILE>);
 close(INFILE);

 undef(@list_type);  # clear 'em for each file
 undef(@list_level);

 # Catch the document meta-information
 # first up, the title!
 if ($instream =~ /<TITLE>([^<]+)<\/TITLE>/i) {
  $title = $1;
 } else {
  $title = $file;
 }
 $title =~ tr/\n{}\\/ ___/; # safetify these kooky illegal characters!

 # second up, the author!
 if ($instream =~ /<LINK\s+REV\s*=\s*MADE\s+HREF\s*=\s*"([^"]+)"/i) {
  $author = $1;
  if ($author =~ /^mailto:/i) {
   $author = $';
  }
 } else {
  $author = '';
 }
 $author =~ tr/\n{}\\/ ___/; # safetify these kooky illegal characters!

 # third up, keywords!
 if ($instream =~ /<META\s+HTTP-EQUIV\s*=\s*"Keywords"\s+Content\s*=\s*"([^"]+)"/i) {
  $keywords = $1;
 } else {
  $keywords = '';
 }
 $keywords =~ tr/\n{}\\/ ___/; # safetify these kooky illegal characters!

 # The time-stamp of the HTML file is copied into the "Creation Time" of
 # the RTF file.  The moment when the conversion happens is stuck into
 # the "Revision Time" of the file, and will be overwritten if/when you
 # make (and save) changes to the RTF file in your word processor.

 ($junk, $junk, $junk, $junk, $junk, $junk, $junk, $junk, $junk, 
        $filetime, $junk, $junk, $junk) = stat($file); 
 # Get the input file's last revision date, in UNIX format

 # Now cook up the init string for this file.
 $myinit = $init . "{\\info \n{\\title $title}\n"
    . "{\\creatim" . &unixtime2rtf($filetime) . "}\n{\\revtim"
    . &unixtime2rtf(time()) . "}\n{\\author $author}\n{\\keywords $keywords}"
    . "{\\doccomm Converted from $file by: $stamp, by Sean M. Burke (sean\@QRD.org)}}\n";

 # OK, end of metainformation gig.

 if ($instream =~ /<BODY[^>]*>/i ) {
  $instream = $';
  $instream =~ s/ *<\/(BODY|HTML)>//ig;
 } else {
  warn "No BODY tag found in $file ... conversion may be deeply flawed.\n";
 }
 $instream =~ s/[{}\\]/\\$&/g; # Escape out brackets and \'s
 
 # $instream =~ s/<!--\s*([^-]*)\s*-->//g;  # Kill SGML comments
 # $instream =~ s/<!--\s*([^-]*)\s*-->/{\\plain \\v $&}/g;  # Kill SGML comments

 # Okay, now we start really chewing on the HTML and chunk by chunk
 # replacing it with the correct RTF code.
  
 $instream =~ s/<(\/PRE|\/[UOD]L|\/H[1-6][^>]*|BLOCKQUOTE|\/BLOCKQUOTE|HR)[^>]*>/$&<P>/ig;
 # put <P>'s after </PRE>s,  close-UL/OL/DLs, close-DL's, 
 #      BLOCKQUOTEs, close-BLOQUOTEs, close-H?s, and HRs

 $instream =~ s/\s*<P>\s*(<H[1-6R][^>]*>)/$1/ig;
 # kill P's before headings or HRs.

 $instream =~ s/<P>[ \t\n]*<(PRE|[UOD]L|LI|HR|BLOCKQUOTE)>/<$1>/ig;
 # kill <P>'s before <PRE>, UL/OL/DLs, DL's, BLOCKQUOTEs, HR's, and LI's

 # Handle whitespace, PREs, and Ps
 $instream =~ s/(<\/?PRE[^>]*>|<PRE>)|(<\/?P[^>]*>)|(\s+)/&parse_p($&)/ieg;
 # Note the extremely powerful use of s/A/&B/ieg as a bogus parser here;
 # this substitutes for a messy while() loop.  Worship s/A/&B/ieg !!

 # Now handle character styles
 $instream =~ s/<$underline_re>\s*/{\\ul /ig;
 $instream =~ s/<$italic_re>\s*/{\\i /ig;
 $instream =~ s/<$bold_re>\s*/{\\b /ig;
 $instream =~ s/\s*<\/$close_re>/}/ig;
 $instream =~ s/<CODE>\s*/{\\f1 /ig;
 $instream =~ s/\s*<\/CODE>/}/ig;
 $instream =~ s/<SUB>\s*/{\\sub /ig;
 $instream =~ s/\s*<\/SUB>/}/ig;
 $instream =~ s/<SUP>\s*/{\\super /ig;
 $instream =~ s/\s*<\/SUP>/}/ig;



 # Now handle the other structural codes
 #  First, headings
 $instream =~ s/<H([1-6])[^>]*>\s*/\n\\par\\pard\\pard$heading_space_before\{\\plain $heading_styles[$1-1]/ig;


 $instream =~ s/<\/H[1-6]>\s*/\}\n/ig;
 #  Now, other structural tags
 $instream =~ s/[ ]*<(HR|BR|P|BLOCKQUOTE|\/BLOCKQUOTE|UL|\/UL|LI|\/LI|DL|DT|DD|\/DL|OL|\/OL)[^>]*>[ ]*/&parse_structure($1)/ieg;


 # Whatever tags are left, hide 'em-- we don't know how to deal with 'em.
 $instream =~ s/<[^>]+>/\{\\plain \\v $&\}/g;

 # Almost there -- resolve entities
 $instream =~ s/\&([^\;]{1,9});/&resolve_entity($1)/eg;

 # Last step-- quote the 8-bit characters
 $instream =~ s/([\x80-\xff])/"\\'".(unpack("H2",$1))/eg;

 ###
 # Output it all
 $outname = $file;
 if ($outname =~ /\.html?/i) {
  $outname =~ s/\.html?/.rtf/i;
 } else {
  $outname .= '.rtf';
 }

 die "Can't open output file $outname" unless open (OUTFILE, "> $outname");
 print "Writing $outname\n" if ($debug > 0);
 print OUTFILE ($myinit);
 print OUTFILE ($instream);
 print OUTFILE ("}\n");
 if ($debug > 1) {
  print "=== $file ===\n$myinit";
  print $instream;
  print "}\n";
 }
 close (OUTFILE);
}
print "Done.\n" if ($debug > 0);

######################################################################

sub parse_p {
 # Deal with whitespace, PRE, and P's.
 # To be called only by the s/A/&B/ieg expression up there.
 # remember that $pre_state is global; its value is 0 or 1
 local($input) = $_[0]; # the thing that matched

 $input =~ tr/a-z/A-Z/;
 if ($input =~ /<PRE/) {   # PRE tags
  $pre_state = 1;
  return "\n\\pard\\par\\f1 ";  # note that a PRE implies a newline
			# also let's switch to the monospace font
 } elsif ($input =~ /<\/PRE/) {  # close PRE's
  $pre_state = 0;
  return '\f0 ';  # back to the proportional font
 } elsif ($input =~ /^<P>|<P[ \n\t]+/) {    # P tags
  $pre_state = 0;
  return '<P>';
 } elsif ($input =~ /^<\/P>/) {  # close-P's
  $pre_state = 0;
  return '';
 } elsif ($input =~ /^[ \n\t]+$/) {   # whitespace
  if ($pre_state == 0) {
   return ' '; # collapse all whitespace
  } else { # we're in a PRE entity-- fiddle with whitespace
   $input =~ s/\n/\n\\pard\\par /g;
   return $input;
  }
 }
}

######################################################################

sub parse_structure {
 # @list_type is global
 # @list_level is global
 # the FIRST element of each list is the most current one.
 local($in_tag) = $_[0];
 local($l_indent, $depth);
 $in_tag =~ tr/a-z/A-Z/;

 $depth = @list_level;  #note that DL doesn't affect this stack
 $l_indent = $tab * $depth;

 if ($in_tag eq 'UL') {
  unshift(@list_level, 0);   #just a placeholder
  unshift(@list_type, 'UL'); #store the list type
  return '';
 } elsif ($in_tag eq 'OL') {
  unshift(@list_level, 0);   #will get incremented
  unshift(@list_type, 'OL'); #store the list type
  return '';
 } elsif ($in_tag eq '/OL' || $in_tag eq '/UL' || $in_tag eq '/BLOCKQUOTE') {
  shift(@list_level);
  shift(@list_type);
  #return '\\par\\pard';

 } elsif ($in_tag eq 'LI') {
  if($list_type[0] eq 'UL') {
   return "\n\\par\\pard\\li$l_indent\\bullet  ";
  } elsif ($list_type[0] eq 'OL') {
   ++$list_level[0];
   return "\n\\par\\pard\\li$l_indent {\\b $list_level[0]}\. ";
  } # else what the hell are we doing saying 'LI'?
 } elsif ($in_tag eq '/LI') {
  #ummm?

 } elsif ($in_tag eq 'BLOCKQUOTE') {
  unshift(@list_level,0);   # a dummy placeholder
  unshift(@list_type,'BLOCKQUOTE');  # not too contentful either
  return '';

 } elsif ($in_tag eq 'DL' || $in_tag eq '/DL') {
  # la la la, I'm doing nothing, la la la.

 } elsif ($in_tag eq 'P' || $in_tag eq 'DT') {
  # note that DT is just like a P
  return "\n\\par\\pard$paragraph_space_before\\li$l_indent ";

 } elsif ($in_tag eq 'DD') {
  # just like a P, but just one more ident level in, and without
  # $paragraph_space_before
  return "\n\\par\\pard\\li" . ($l_indent + $tab) . ' ';

 } elsif ($in_tag eq '/DT') {
  # ummm?
 } elsif ($in_tag eq '/DD') {
  # ummm?

 } elsif ($in_tag eq 'BR') {
  return "\n\\par\\pard\\li$l_indent ";

 } elsif ($in_tag eq 'HR') {
  return "\n\\par\\pard\\li$l_indent $hr_style ";
  # note that there is indenting-- so that a HR in the middle of a list
  # can be centered differently from one outside a list
 }

 return '';
}

######################################################################
sub unixtime2rtf {
 local($intime, $sec, $min, $hr, $dy, $mo, $yr, $junk);

 $intime = $_[0];

 ($sec, $min, $hr, $dy, $mo, $yr, $junk, $junk, $junk) = localtime($intime);
 # Note that this is local time.

 ++$mo;  # Note that PERL counts months from January=0
         #  but RTF counts from January=1
 $yr += 1900;

 return "\\yr$yr\\mo$mo\\dy$dy\\hr$hr\\min$min\\sec$sec";
}

######################################################################
sub resolve_entity {
    local($in, $out);
    $in = $_[0];

    $out = $entities{$in};
    if (defined($out)) { #easily resolvable
	return $out;
    } elsif ($in =~ /^\#([0-9]+)$/) {
	return pack("C", $1);
    } else {
	return '&' . $in . ';'; #make it unchanged.
    }

}

######################################################################


