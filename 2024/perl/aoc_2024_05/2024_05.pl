#!/usr/bin/perl

use warnings;
use strict;

use Data::Dumper;

my $year = 2024;
my $day  = 5;

my @expectedResults = ( [ 1, 143, 123 ], [ 0, 6498, 5017 ], );

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

    my %positions = ();
    my @orders    = ();
    for my $line (@$lines) {
        if ( $line =~ /(\d+)\|(\d+)/ ) {
            my ( $left, $right ) = ( $1, $2 );
            if ( $positions{$left} ) {
                push @{ $positions{$left} }, $right;
            }
            else {
                $positions{$left} = [$right];
            }
        }
        elsif ( $line =~ /\d+,\d+/ ) {
            push @orders, [ split( /,/, $line ) ];
        }
    }

    my $sum = 0;

    for my $order (@orders) {
        my @pageOrder = sort {
            ( grep { $a == $_ } @{ $positions{$b} } )
              ? 1
              : ( ( grep { $b == $_ } @{ $positions{$a} } ) ? -1 : 0 )
        } grep {
            my $p = $_;
            grep { $p == $_ } @$order
        } keys %positions;

        my $equal = 1;
        for my $i ( 0 .. $#pageOrder ) {
            $equal = 0 unless $pageOrder[$i] == $order->[$i];
        }
        $sum += $order->[ ( $#$order + 1 ) / 2 ] if $equal;
    }

    return $sum;
};

my $run2 = sub {
    my $lines = shift;

    my %positions = ();
    my @orders    = ();
    for my $line (@$lines) {
        if ( $line =~ /(\d+)\|(\d+)/ ) {
            my ( $left, $right ) = ( $1, $2 );
            if ( $positions{$left} ) {
                push @{ $positions{$left} }, $right;
            }
            else {
                $positions{$left} = [$right];
            }
        }
        elsif ( $line =~ /\d+,\d+/ ) {
            push @orders, [ split( /,/, $line ) ];
        }
    }

    my $sum = 0;

    for my $order (@orders) {
        my @pageOrder = sort {
            ( grep { $a == $_ } @{ $positions{$b} } )
              ? 1
              : ( ( grep { $b == $_ } @{ $positions{$a} } ) ? -1 : 0 )
        } grep {
            my $p = $_;
            grep { $p == $_ } @$order
        } keys %positions;

        my $equal = 1;
        for my $i ( 0 .. $#pageOrder ) {
            $equal = 0 unless $pageOrder[$i] == $order->[$i];
        }
        $sum += $pageOrder[ ( $#$order + 1 ) / 2 ] unless $equal;
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
