#!/usr/bin/perl

use warnings;
use strict;

use Data::Dumper;

my $year = 2024;
my $day  = 2;

my @expectedResults = ( [ 1, 2, 4 ], [ 0, 502, 544 ], );

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

    my @levels = map { [ split /\s+/ ] } @$lines;

    my $count = 0;
    for my $levelLine (@levels) {
        my $lastLevel = undef;
        my $lastSign  = undef;
        my $ok        = 1;

        for my $level (@$levelLine) {
            if ( defined $lastLevel ) {
                ;
                if ( abs( $level - $lastLevel ) > 3 || $level == $lastLevel ) {
                    $ok = 0;
                    last;
                }
                my $sign = ( $level - $lastLevel ) / abs( $level - $lastLevel );
                if ( $lastSign && $sign != $lastSign ) {
                    $ok = 0;
                    last;
                }
                $lastSign = $sign;
            }
            $lastLevel = $level;
        }
        $count++ if $ok;
    }

    return $count;
};

my $run2 = sub {
    my $lines = shift;

    my @levels = map { [ split /\s+/ ] } @$lines;

    my $count = 0;
    for my $levelLine (@levels) {

        sub testLevels {
            my $levelLine = shift;
            my $lastLevel = undef;
            my $lastSign  = undef;
            for my $level (@$levelLine) {
                if ( defined $lastLevel ) {
                    return 0
                      if ( abs( $level - $lastLevel ) > 3
                        || $level == $lastLevel );
                    my $sign =
                      ( $level - $lastLevel ) / abs( $level - $lastLevel );
                    return 0 if ( $lastSign && $sign != $lastSign );
                    $lastSign = $sign;
                }
                $lastLevel = $level;
            }
            return 1;
        }

        my @testLines = ($levelLine);
        for ( my $i = 0 ; $i <= $#$levelLine ; $i++ ) {
            push @testLines,
              [
                @$levelLine[ 0 .. $i - 1 ],
                @$levelLine[ $i + 1 .. $#$levelLine ]
              ];
        }
        for my $levelLine_ (@testLines) {
            if ( testLevels($levelLine_) ) {
                $count++;
                last;
            }
        }
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
