#!/usr/bin/perl -w
use strict;
use warnings;

my $start_time=localtime();
print "Start time: $start_time\n";
#directories

my $reference_dir="";
my $software_dir="";
my $ref_genome=$ARGV[3]; #"indica/ir64";
my $reference_seq=$ARGV[2]; #"os.ir64.cshl.draft.1.0.scaffold.fa";
my $samtools="";
my $gatk="";
my $java_memory="-Xmx8g";
my $vcf_out_mode="EMIT_ALL_SITES";

my $output_dir=$ARGV[0];
my $raw_dir=$ARGV[1];

my $fp = 'config';
open my $info, $fp or die "Could not open $fp: $!";

while( my $line = <$info>)  {
        if ($line =~ m/reference_dir/) {
                $reference_dir=(split '=', $line)[-1];
                chomp($reference_dir);           
        }
	elsif($line =~ m/gatk/){
                $gatk=(split '=', $line)[-1];
                chomp($gatk);           
        }
	elsif($line =~ m/software_dir/){
                $software_dir=(split '=', $line)[-1];
                chomp($software_dir);
        }
	elsif($line =~ m/samtools/){
                $samtools=(split '=', $line)[-1];
                chomp($samtools);
        }
}
close($fp);


#print "Removing intermdediate files...\n";
#system("rm $output_dir/$raw_dir/*.sam");
#print "SAM files removed.\n";
#system("rm $output_dir/$raw_dir/*.fxmt.ba*");
#print "Fixmate BAM files removed.\n";
#system("rm $output_dir/$raw_dir/*.mkdup.ba*");
#print "Mark duplicate BAM files removed.\n";
#system("rm $output_dir/$raw_dir/*.addrep.ba*");
#print "Add replaced BAM files removed.\n";
#system("rm $output_dir/$raw_dir/*.metrics");
#print "Metrics files removed.\n";
#system("rm $output_dir/$raw_dir/*.list");
#print "List files removed.\n";

my $input = 'input.info';
my $count="";
my $genome="";

open FILE, $input or die $!;
while (my $data=readline*FILE){
	$data=~/(.*):(.*)/;
	$genome=$1;
	$count=$2;

	if($raw_dir eq $genome){

		if($count > 2){
			my $merge_bam="$raw_dir.merged.bam";
			if (-e "$output_dir/$raw_dir/$merge_bam"){
				print "$merge_bam already exists.\n";
			} else {
				print "Merging realigned BAM files...\n";
				system("samtools merge $output_dir/$raw_dir/$merge_bam $output_dir/$raw_dir/*.realign.bam");
				print "Realigned BAM files merged into $merge_bam.\n";
			}
			if (-e "$output_dir/$raw_dir/$merge_bam.bai"){
				print "$merge_bam.bai already exists.\n";
			} else {
				system("samtools index $output_dir/$raw_dir/$merge_bam");
				print "$merge_bam indexed.\n";
			}

			#remove intermediate files
			system("rm $output_dir/$raw_dir/*.list");
			system("rm $output_dir/$raw_dir/*.realign.bam");
			system("rm $output_dir/$raw_dir/*.realign.bai");
		}
	}
}
close FILE;

#my $snp_calling_output="$raw_dir.vcf";
#print "Calling variants...\n";
#system("java $java_memory -XX:ParallelGCThreads=2 -jar $software_dir/$gatk/GenomeAnalysisTK.jar -T UnifiedGenotyper -nt 10 -R $reference_dir/$ref_genome/$reference_seq -I $output_dir/$raw_dir/$merge_bam -o $output_dir/$raw_dir/$snp_calling_output -glm BOTH -mbq 20 --genotyping_mode DISCOVERY -out_mode $vcf_out_mode");

#print "Compressing VC2F file...\n";
#system("/home/jdetras/software/samtools-1.0/htslib-1.0/./bgzip $output_dir/$raw_dir/$snp_calling_output");

my $end_time=localtime();
print "End time: $end_time. Done.\n";
exit();
