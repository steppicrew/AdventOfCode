#!/usr/bin/perl

use warnings;
use strict;

use Data::Dumper;

my $year = 2024;
my $day  = 3;

my @expectedResults =
  ( [ 1, 161, 161 ], [ 2, 161, 48 ], [ 0, 160672468, 84893551 ] );

sub readInput {
    my $ref           = shift;
    my $inputFilename = __FILE__;
    $inputFilename =~ s/\.pl$//;
    $inputFilename .= "_ref$ref" if $ref;
    $inputFilename .= ".txt";
    open( my $fh, "<", $inputFilename )
      or die "Could not open $inputFilename";
    my $lines = [ grep { $_ } map { chomp; $_ } <$fh> ];
    close $fh;
    return $lines;
}

my $run1 = sub {
    my $lines = shift;

    my $line = join( "", @$lines );

    my $sum = 0;
    while ( $line =~ s/mul\((\d{1,3}),(\d{1,3})\)// ) {
        $sum += $1 * $2;
    }

    return $sum;
};

my $run2 = sub {
    my $lines = shift;

    my $line = join( "", @$lines );

    my @dos = map { $_ =~ s/don\'t\(\).*//; $_ } split( /do\(\)/, $line );

    my $sum = 0;
    for my $do (@dos) {
        while ( $do =~ s/mul\((\d{1,3}),(\d{1,3})\)// ) {
            $sum += $1 * $2;
        }
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
