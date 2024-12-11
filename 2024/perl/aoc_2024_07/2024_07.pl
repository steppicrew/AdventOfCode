#!/usr/bin/perl

use warnings;
use strict;

use Data::Dumper;

$| = 1;

my $year = 2024;
my $day  = 7;

my @expectedResults =
  ( [ 1, 3749, 11387 ], [ 0, 882304362421, 145149066755184 ], );

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

    my @values = map {
        /(\d+): (.*)/;
        [ $1, [ split( /\s+/, $2 ) ] ]
    } @$lines;

    my @operations = (
        sub {
            my $a = shift;
            my $b = shift;
            $a + $b;
        },
        sub {
            my $a = shift;
            my $b = shift;
            $a * $b;
        },
    );

    my $test;
    $test = sub {
        my $result    = shift;
        my $left      = shift;
        my @remaining = @_;
        return $left == $result ? 1 : 0 unless @remaining;
        my ( $right, @newRemaining ) = @remaining;
        for my $op (@operations) {
            my $newLeft = $op->( $left, $right );
            return 1 if $test->( $result, $newLeft, @newRemaining );
        }
        return 0;
    };

    my $sum = 0;
    for my $values (@values) {
        $sum += $values->[0] if $test->( $values->[0], @{ $values->[1] } );
    }

    return $sum;
};

my $run2 = sub {
    my $lines = shift;

    my @values = map {
        /(\d+): (.*)/;
        [ $1, [ split( /\s+/, $2 ) ] ]
    } @$lines;

    my @operations = (
        sub {
            my $a = shift;
            my $b = shift;
            $a + $b;
        },
        sub {
            my $a = shift;
            my $b = shift;
            $a * $b;
        },
        sub {
            my $a = shift;
            my $b = shift;
            "$a$b";
        }
    );

    my $test;
    $test = sub {
        my $result    = shift;
        my $left      = shift;
        my @remaining = @_;
        return $left == $result ? 1 : 0 unless @remaining;
        my ( $right, @newRemaining ) = @remaining;
        for my $op (@operations) {
            my $newLeft = $op->( $left, $right );
            return 1 if $test->( $result, $newLeft, @newRemaining );
        }
        return 0;
    };

    my $sum = 0;
    for my $values (@values) {
        $sum += $values->[0] if $test->( $values->[0], @{ $values->[1] } );
    }

    return $sum;
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
