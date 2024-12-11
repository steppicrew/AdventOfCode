#!/usr/bin/perl

use warnings;
use strict;

use Data::Dumper;

$| = 1;

my $year = 2024;
my $day  = 8;

my @expectedResults = ( [ 1, 14, 34 ], [ 0, 252, 839 ],, );

sub readInput {
    my $ref           = shift;
    my $inputFilename = __FILE__;
    $inputFilename =~ s/\.pl$//;
    $inputFilename .= "_ref$ref" if $ref;
    $inputFilename .= ".txt";
    open( my $fh, "<", $inputFilename ) or die "Could not open $inputFilename";
    my $lines = [ grep { $_ } map { chomp; $_ } <$fh> ];
    close $fh;
    return $lines;
}

my $run1 = sub {
    my $lines = shift;

    my %antennas = ();
    for my $row ( 0 .. $#$lines ) {
        my @line = split( //, $lines->[$row] );
        for my $col ( 0 .. $#line ) {
            next if $line[$col] eq '.';
            if ( $antennas{ $line[$col] } ) {
                push @{ $antennas{ $line[$col] } }, [ $col, $row ];
            }
            else {
                $antennas{ $line[$col] } = [ [ $col, $row ] ];
            }
        }
    }

    my ( $maxX, $maxY ) = ( scalar( split( //, $lines->[0] ) ) - 1, $#$lines );

    my %antinodes = ();

    my $test = sub {
        my $x = shift;
        my $y = shift;
        $antinodes{"$x,$y"} = undef
          unless $x < 0 || $x > $maxX || $y < 0 || $y > $maxY;
    };

    for my $antennas ( values %antennas ) {
        for my $a1 (@$antennas) {
            for my $a2 (@$antennas) {
                next if $a1->[0] == $a2->[0] && $a1->[1] == $a2->[1];
                my $dx = $a2->[0] - $a1->[0];
                my $dy = $a2->[1] - $a1->[1];
                $test->( $a1->[0] - $dx,     $a1->[1] - $dy );
                $test->( $a1->[0] + 2 * $dx, $a1->[1] + 2 * $dy );
            }
        }

    }

    return scalar( keys %antinodes );
};

my $run2 = sub {
    my $lines = shift;

    my %antennas = ();
    for my $row ( 0 .. $#$lines ) {
        my @line = split( //, $lines->[$row] );
        for my $col ( 0 .. $#line ) {
            next if $line[$col] eq '.';
            if ( $antennas{ $line[$col] } ) {
                push @{ $antennas{ $line[$col] } }, [ $col, $row ];
            }
            else {
                $antennas{ $line[$col] } = [ [ $col, $row ] ];
            }
        }
    }

    my ( $maxX, $maxY ) = ( scalar( split( //, $lines->[0] ) ) - 1, $#$lines );

    my %antinodes = ();

    my $test = sub {
        my $x = shift;
        my $y = shift;
        $antinodes{"$x,$y"} = undef
          unless $x < 0 || $x > $maxX || $y < 0 || $y > $maxY;
    };

    my $normalize = sub {
        my $dx  = shift;
        my $dy  = shift;
        my $min = $dx < $dy ? $dx : $dy;
        for my $i ( reverse( 2 .. $min ) ) {
            return ( $dx / $i, $dy / $i ) if $dx % $i == 0 && $dy % $i == 0;
        }
        return ( $dx, $dy );
    };

    for my $antennas ( values %antennas ) {
        for my $a1 (@$antennas) {
            for my $a2 (@$antennas) {
                next if $a1->[0] == $a2->[0] && $a1->[1] == $a2->[1];
                my ( $dx, $dy ) =
                  $normalize->( $a2->[0] - $a1->[0], $a2->[1] - $a1->[1] );
                for my $i ( -$maxX .. $maxX ) {
                    $test->( $a1->[0] + $i * $dx, $a1->[1] + $i * $dy );
                }
            }
        }

    }

    return scalar( keys %antinodes );
};

sub run {
    my ( $ref, $run, $fn, $expectedResult, $lines ) = @_;
    my $result = $fn->($lines);
    print( $ref ? "ref$ref/$run: " : "main/$run: " );
    if ( !defined($expectedResult) ) {
        print("? ($result)");
    }
    elsif ( $result == $expectedResult ) {
        print("✔ ($result)");
    }
    else {
        print("✗\n\tExpected: $expectedResult\n\tGot: $result");
    }
    print("\n");
}

foreach my $expectedResult (@expectedResults) {
    my ( $ref, $expectedResult1, $expectedResult2 ) = @$expectedResult;
    my $lines = readInput($ref);
    run( $ref, 1, $run1, $expectedResult1, $lines );
    run( $ref, 2, $run2, $expectedResult2, $lines );
}
