import React, {useState} from 'react';
import { Card, CardContent } from '@mui/material';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function PlaceInfo({place, openInfo, setSelectedPlace, setPlaceReviews, reviews}) {
    const [prevPlace, setPrevPlace] = useState(place);
    const [prevReviews, setPrevReviews] = useState(reviews);

    // DB에 쿼리 또는 검색 api로 결과 받아옴
    const handleOpenInfo = () => {
        setSelectedPlace(place)
        setPrevPlace(place)
        console.log(place);

        fetch(`/review/${place.id}`)
            .then((r) => r.json())
            .then((r) => {
                console.log(r);
                setPlaceReviews(r);
                setPrevReviews(r);
            })
            .catch((e) => console.log("error when load reviews"));
        
            openInfo(true);
    }


    return (
            <Card sx={{
                display : 'flex',
                mx: 'auto',
                '&:hover': {
                    backgroundColor: '#f5f5f5',
                },
                }} onClick={handleOpenInfo}>

                <Box sx={{ 
                display: 'flex', 
                flexDirection: 'column', 
                width: 500,
                }}>
                <CardContent sx = {{flex: '1 0 auto'}}>
                <Typography variant="h6"> {place.name} </Typography>
                <Typography variant="subtitle2" color="text.secondory"> {place.type}  ({place.numReviews})  ★ {place.avgRating}</Typography>
                <Typography variant="caption" color="text.secondory"> {place.location} </Typography>
                </CardContent>
                </Box>
            </Card>
    )
}