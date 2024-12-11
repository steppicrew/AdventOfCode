#!/usr/bin/perl

use warnings;
use strict;

use Data::Dumper;

my $year = 2024;
my $day  = 4;

my @expectedResults = ( [ 1, 18, 9 ], [ 0, 2644, 1952 ] );

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

    my %map = ();
    for my $row ( 0 .. $#$lines ) {
        my @line = split '', $lines->[$row];
        for my $col ( 0 .. $#line ) {
            $map{"$col,$row"} = $line[$col];
        }
    }

    my @directions = (
        [ 1,  0 ], [ 1,  1 ],  [ 0, 1 ],  [ -1, 1 ],
        [ -1, 0 ], [ -1, -1 ], [ 0, -1 ], [ 1,  -1 ],
    );

    my $testPos = sub {
        my $pos       = shift;
        my $direction = shift;
        my $factor    = shift;
        my $letter    = shift;

        $pos =~ /(\d+),(\d+)/;
        my ( $x, $y ) = ( $1, $2 );

        $x += $factor * $direction->[0];
        $y += $factor * $direction->[1];
        defined $map{"$x,$y"} && $map{"$x,$y"} eq $letter;
    };

    my $test = sub {
        my $pos   = shift;
        my $count = 0;
        for my $direction (@directions) {
            $count++
              if $testPos->( $pos, $direction, 0, "X" )
              && $testPos->( $pos, $direction, 1, "M" )
              && $testPos->( $pos, $direction, 2, "A" )
              && $testPos->( $pos, $direction, 3, "S" );
        }
        return $count;
    };

    my $count = 0;
    for my $pos ( keys %map ) {
        $count += $test->($pos);
    }

    return $count;
};

my $run2 = sub {
    my $lines = shift;

    my %map = ();
    for my $row ( 0 .. $#$lines ) {
        my @line = split '', $lines->[$row];
        for my $col ( 0 .. $#line ) {
            $map{"$col,$row"} = $line[$col];
        }
    }

    my @directions = ( [ 1, 1 ], [ -1, 1 ], [ -1, -1 ], [ 1, -1 ], );

    my $testPos = sub {
        my $pos       = shift;
        my $direction = shift;
        my $factor    = shift;
        my $letter    = shift;

        $pos =~ /(\d+),(\d+)/;
        my ( $x, $y ) = ( $1, $2 );

        $x += $factor * $direction->[0];
        $y += $factor * $direction->[1];
        defined $map{"$x,$y"} && $map{"$x,$y"} eq $letter;
    };

    my $test = sub {
        my $pos   = shift;
        my $count = 0;
        for my $direction (@directions) {
            $count++
              if $testPos->( $pos, $direction, -1, "M" )
              && $testPos->( $pos, $direction, 0,  "A" )
              && $testPos->( $pos, $direction, 1,  "S" );
        }
        return $count == 2 ? 1 : 0;
    };

    my $count = 0;
    for my $pos ( keys %map ) {
        $count += $test->($pos);
    }

    return $count;
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
