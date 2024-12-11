#!/usr/bin/perl

use warnings;
use strict;

use Data::Dumper;

$| = 1;

my $year = 2024;
my $day  = 6;

my @expectedResults = ( [ 1, 41, 6 ], [ 0, 5131, 1784 ] );

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
    my @startPos;
    for my $row ( 0 .. $#$lines ) {
        my @chars = split( //, $lines->[$row] );
        for my $col ( 0 .. $#chars ) {
            $map{"$col,$row"} = $chars[$col];
            @startPos = ( $col, $row ) if $chars[$col] eq '^';
        }
    }

    my @directions = ( [ 0, -1 ], [ 1, 0 ], [ 0, 1 ], [ -1, 0 ] );

    my $directionIndex = 0;
    my $direction      = $directions[0];
    my @pos            = @startPos;
    my %visited        = ( "$pos[0],$pos[1]" => undef );
    while (1) {
        my @nextPos = ( $pos[0] + $direction->[0], $pos[1] + $direction->[1] );
        my $index   = "${nextPos[0]},${nextPos[1]}";
        my $char    = $map{$index};
        last unless $char;
        if ( $char eq '#' ) {
            $directionIndex++;
            $direction =
              $directions[ $directionIndex % ( scalar @directions ) ];
        }
        else {
            $visited{$index} = undef;
            @pos = @nextPos;
        }
    }

    return scalar keys %visited;
};

my $run2 = sub {
    my $lines = shift;

    my %map = ();
    my @startPos;
    for my $row ( 0 .. $#$lines ) {
        my @chars = split( //, $lines->[$row] );
        for my $col ( 0 .. $#chars ) {
            $map{"$col,$row"} = $chars[$col];
            @startPos = ( $col, $row ) if $chars[$col] eq '^';
        }
    }

    my @directions = ( [ 0, -1 ], [ 1, 0 ], [ 0, 1 ], [ -1, 0 ] );

    my $test = sub {
        my $newObstacle = shift;
        return 0 unless $map{$newObstacle} eq ".";

        my $directionIndex = 0;
        my $direction      = $directions[0];
        my @pos            = @startPos;
        my %visited        = ( "$pos[0],$pos[1]" => 1 );
        while (1) {
            my @nextPos =
              ( $pos[0] + $direction->[0], $pos[1] + $direction->[1] );
            my $index = "${nextPos[0]},${nextPos[1]}";
            my $char  = $map{$index};
            return 0 unless $char;
            if ( $char eq '#' || $index eq $newObstacle ) {
                $directionIndex++;
                $direction =
                  $directions[ $directionIndex % ( scalar @directions ) ];
            }
            else {
                my $vIndex =
                  "$index," . $direction->[0] . "," . $direction->[1];
                return 1 if $visited{$vIndex};
                $visited{$vIndex} = 1;
                @pos = @nextPos;
            }
        }
    };

    my $count = 0;
    for my $obstacle ( keys %map ) {
        $count++ if $test->($obstacle);
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
