# Function for drawing arrows on paths
arrowLine <- function(x, y, color,N=2){
  lengths <- c(0, sqrt(diff(x)^2 + diff(y)^2))
  l <- cumsum(lengths)
  tl <- l[length(l)]
  el <- seq(0, to=tl, length=N+1)[-1]

  for(ii in el){

    int <- findInterval(ii, l)
    xx <- x[int:(int+1)]
    yy <- y[int:(int+1)]

    ## points(xx,yy, col="grey", cex=0.5)

    dx <- diff(xx)
    dy <- diff(yy)
    new.length <- ii - l[int]
    segment.length <- lengths[int+1]

    ratio <- new.length / segment.length

    xend <- x[int] + ratio * dx
    yend <- y[int] + ratio * dy
    #points(xend,yend, col="white", pch=19)
    arrows(x[int], y[int], xend, yend, length=0.1,col=color)

  }

}


# Limits for certain zooms on continents

xlim_europe <- c(-25, 45)
ylim_europe <- c(35, 71)

# Create palette for paths based on counts
pal <- colorRampPalette(c("#f2f2f2","green"))
colors <- pal(100)
maxcnt <- max(nobel$cnt)

# Generate map
map('world',col='#787878',fill=TRUE,bg='black',lwd=0.20,xlim=xlim_europe,ylim=ylim_europe)

# Sort by count so most common paths are on top
nobel <- nobel[order(nobel$cnt),]

# Loop over unique paths
for (j in 1:length(nobel$lon1)) {
    # Compute great circle
    inter<-gcIntermediate(c(nobel$lon1[j],nobel$lat1[j]),c(nobel$lon2[j],nobel$lat2[j]),n=500,addStartEnd=TRUE,breakAtDateLine=TRUE)
    colindex <- round( (nobel$cnt[j] / maxcnt) * length(colors) )
    # Break line if it crosses International Date Line; draw in two pieces
    if(length(inter)==2){
        lines(inter[[1]],col=colors[colindex],lwd=1.2)
        lines(inter[[2]],col=colors[colindex],lwd=1.2)
    }
    # Draw single line if it doesn't cross IDL
    else{
        lines(inter,col=colors[colindex],lwd=1.2)
        arrowLine(inter[,1],inter[,2],colors[colindex])
    }
}

# Laureates who died in their birth country or are not dead

# load file
nobel_points <- read.table('../data/points_r.csv',header=TRUE)
nobel_points <- nobel_points[order(nobel_points$cnt),]

# Loop over unique points
for (j in 1:length(nobel_points$lon1)) {
    size_points <- log10(nobel_points$cnt[j]) + 1
    points(x=nobel_points$lon1[j],y=nobel_points$lat1[j],pch=21,col="orange",cex=size_points)
}

# title
title(main='Nobel laureate emigration patterns',col.main="white",sub="1901-2013",col.sub="white")

# legend
legend(60, -15, c("1", "10", "100"), col = "orange", text.col = "black", pch = 21, y.intersp=1.3,cex = 0.8, pt.cex=c(1,2,3), bg = "gray90")
