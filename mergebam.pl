#!/usr/bin/perl -w
use strict;

my $starttime=localtime();
print "Start time: $starttime\n";
#directories

my $reference_dir="";
my $software_dir="";
my $ref_sequence=$ARGV[2]; #"os.ir64.cshl.draft.1.0.scaffold.fa";
my $ref_genome=$ARGV[3]; #"indica/ir64";
my $samtools="";
my $gatk="";
my $javaMemory="-Xmx8g";
my $vcfOutMode="EMIT_ALL_SITES";

my $output_dir=$ARGV[0];
my $raw_dir=$ARGV[1];

my $fp = 'config';
open my $info, $fp or die "Could not open $fp: $!";

while(my $line = <$info>)  {
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
	elsif($line =~ m/samtool=/){
                $samtools=(split '=', $line)[-1];
                chomp($samtools);
        }
}

#print "Removing intermdediate files...\n";
#system("rm $outputDir/$rawDir/*.sam");
#print "SAM files removed.\n";
#system("rm $outputDir/$rawDir/*.fxmt.ba*");
#print "Fixmate BAM files removed.\n";
#system("rm $outputDir/$rawDir/*.mkdup.ba*");
#print "Mark duplicate BAM files removed.\n";
#system("rm $outputDir/$rawDir/*.addrep.ba*");
#print "Add replaced BAM files removed.\n";
#system("rm $outputDir/$rawDir/*.metrics");
#print "Metrics files removed.\n";
#system("rm $outputDir/$rawDir/*.list");
#print "List files removed.\n";

my $mergeBam="$raw_dir.merged.bam";
if (-e "$output_dir/$raw_dir/$mergeBam"){
	print "$mergeBam already exists.\n";
} else {
	print "Merging realigned BAM files...\n";
	system("samtools merge $output_dir/$raw_dir/$mergeBam $output_dir/$raw_dir/*.realign.bam");
	print "Realigned BAM files merged into $mergeBam.\n";
}
if (-e "$output_dir/$raw_dir/$mergeBam.bai"){
	print "$mergeBam.bai already exists.\n";
} else {
	system("samtools index $output_dir/$raw_dir/$mergeBam");
	print "$mergeBam indexed.\n";
}

#remove intermediate files
system("rm $output_dir/$raw_dir/*.list");
system("rm $output_dir/$raw_dir/*.realign.bam");
system("rm $output_dir/$raw_dir/*.realign.bai");

#my $snp_calling_output="$rawDir.vcf";
#print "Calling variants...\n";
#system("java $javaMemory -XX:ParallelGCThreads=2 -jar $softwareDir/$gatk/GenomeAnalysisTK.jar -T UnifiedGenotyper -nt 10 -R $refDir/$refGenome/$refSeq -I $outputDir/$rawDir/$mergeBam -o $outputDir/$rawDir/$snp_calling_output -glm BOTH -mbq 20 --genotyping_mode DISCOVERY -out_mode $vcfOutMode");

#print "Compressing VCF file...\n";
#system("/home/jdetras/software/samtools-1.0/htslib-1.0/./bgzip $outputDir/$rawDir/$snp_calling_output");

my $endtime=localtime();
print "End time: $endtime. Done.\n";
exit();
