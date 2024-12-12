# Get the JobID from the command line arguments
args <- commandArgs(trailingOnly = TRUE)
jobID <- args[1]

setwd(file.path("/pubapps/mingyi.xie/clashhub/prod/app/TemporaryStorage/", jobID)) 
getwd()
library(DESeq2) 
library(pheatmap)
library(ggplot2)

counts <- read.csv("gene_count_reordered.csv", row.names=1, check.names=FALSE)
coldata <- read.csv("coldata_SampleName.csv", row.names=1, check.names=FALSE)

# Create DESeq2 dataset
counts[is.na(counts)] <- 0
dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata, design = ~ condition)
# Filter out genes (you've set the threshold to >0 to include all genes)
dds <- dds[rowSums(counts(dds)) > 0, ]
# Perform differential expression analysis
dds <- DESeq(dds)
# Extract results 
res <- results(dds) 
# Order results by adjusted p-value
resOrdered <- res[order(res$padj), ]

# Convert to data frame
resOrderedDF <- as.data.frame(resOrdered)

# Reset row names to a column named 'GeneID|GeneName'
resOrderedDF$`GeneID|GeneName` <- rownames(resOrderedDF)

# Extract 'GeneName' and add as a separate column
resOrderedDF$GeneName <- sapply(strsplit(resOrderedDF$`GeneID|GeneName`, "\\|"), function(x) x[2])

# Reorder columns to place 'GeneID|GeneName' and 'GeneName' at the beginning
resOrderedDF <- resOrderedDF[, c("GeneID|GeneName", "GeneName", setdiff(names(resOrderedDF), c("GeneID|GeneName", "GeneName")))]

# Print top 10 rows before writing to CSV
print(head(resOrderedDF, 10))

# Write to CSV without row names since 'GeneID|GeneName' is now a column
write.csv(resOrderedDF, file='differential_expression_results.csv', row.names=FALSE, col.names=TRUE)
