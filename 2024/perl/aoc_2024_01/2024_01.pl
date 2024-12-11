#!/usr/bin/perl

use warnings;
use strict;

use Data::Dumper;

my $year = 2024;
my $day  = 1;

my @expectedResults = ( [ 1, 11, 31 ], [ 0, 1889772, 23228917 ], );

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
    my @left  = ();
    my @right = ();

    for my $line (@$lines) {
        if ( $line =~ /(\d+)\s+(\d+)/ ) {
            push @left,  $1;
            push @right, $2;
        }
    }
    @left  = sort { $a <=> $b } @left;
    @right = sort { $a <=> $b } @right;

    my $sum = 0;
    for my $i ( 0 .. $#left ) {
        $sum += abs( $left[$i] - $right[$i] );
    }

    return $sum;
};

my $run2 = sub {
    my $lines = shift;
    my @left  = ();
    my %right = ();

    for my $line (@$lines) {
        if ( $line =~ /(\d+)\s+(\d+)/ ) {
            push @left, $1;
            $right{$2} = ( $right{$2} || 0 ) + 1;
        }
    }

    my $sum = 0;
    for my $left (@left) {
        $sum += $left * ( $right{$left} || 0 );
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
