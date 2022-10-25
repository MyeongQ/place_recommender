import * as React from 'react';
import PlaceInfo from './PlaceInfo';
import ReviewCard from './ReviewCard';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import TextField from '@mui/material/TextField'
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import SearchIcon from '@mui/icons-material/Search';
import { ExpandMore } from '@mui/icons-material';
import Collapse from '@mui/material/Collapse';
import ClearIcon from '@mui/icons-material/Clear';
import {Card, CardHeader, Avatar, CardContent, CardActions } from '@mui/material';
import { red } from '@mui/material/colors';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import Rating from '@mui/material/Rating';
import InputBase from '@mui/material/InputBase';
import DirectionsIcon from '@mui/icons-material/Directions';

const drawerWidth = 400;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  textAlign: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

export default function PersistentDrawerLeft(onSearch) {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);
  const [infoOpen, setInfoOpen] = React.useState(false);
  const [listOpen, setListOpen] = React.useState([true, false, false]);
  const [searchWord, setSearchWord] = React.useState("");
  const [searchResult, setSearchResult] = React.useState([]);
  const [recommendResult, setRecommendResult] = React.useState([]);
  const [myPlaceResult, setMyPlaceResult] = React.useState([]);
  const [selectedPlace, setSelectedPlace] = React.useState([]);
  const [placeReviews, setPlaceReviews] = React.useState([]);
  //{id: 65541, content: 'Lorem ipsum dolor sit amet, consectetur adipiscing…lentesque et consectetur sem, at ultrices libero.', rating: 4, img: null, createdAt: '2022-10-23T22:45:00.000Z', updatedAt: '2022-10-23T22:45:00.000Z', createdAt: null},
  //{id: 65551, content: 'Lorem ipsum dolor sit amet, consectetur adipiscing…lentesque et consectetur sem, at ultrices libero.', rating: 4, img: null, createdAt: '2022-10-23T22:45:00.000Z', updatedAt: '2022-10-23T22:45:00.000Z', createdAt: null}
  
  const [rating, setRating] = React.useState(3);
  const [myReview, setMyReview] = React.useState(["좋네요~"]);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleInfoDrawerOpen = () => {
    console.log(selectedPlace);
    fetch(`/review/${selectedPlace.id}`)
      .then((r) => r.json())
      .then((r) => {
        console.log(r);
        setPlaceReviews(r);
      })
      .catch((e) => console.log("error when load reviews"));
    setInfoOpen(true);

  };

  const handleInfoDrawerClose = () => {
    setInfoOpen(false);
  };

  const handleClick = (index) => {
    var newList = [false, false, false];
    newList[index] = true;
    setListOpen(newList);
    if(index === 1) {
      fetch("/recommend")
        .then((r) => r.json())
        .then((r) => {
          console.log(r);
          setRecommendResult(r);
        })
        .catch((e) => console.log("error when recommend places"));
    }
  };

  const handleSearch = (event) => {
    event.preventDefault();
    console.log(searchWord);
    fetch(`/search/${searchWord}`)
      .then((r) => r.json())
      .then((r) => {
        console.log(r);
        setSearchResult(r);
        setSearchWord("");
      })
      .catch((e) => console.log("error when search places"));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(myReview);
    // fetch(`/review/:${placeId}/:${myReview}`)
    fetch(`/review/${selectedPlace.id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: myReview,
        rating,
      }),
    }).then((res) => {
        if(res.ok) {
          alert("리뷰가 등록되었습니다.")
        }
        setMyReview("")
      })
      .catch((e) => console.log("error when subit my review"));
  }

  const handleSearchTextChange = (event) => {
    setSearchWord(event.target.value);
  };
  const handleReviewChange = (event) => {
    setMyReview(event.target.value);
  }


  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" open={open}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: 'none' }) }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            여행지 추천 시스템
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader>
          <TextField
            fullWidth
            label="여행지 검색하기"
            id="filled-hidden-label-small"
            type="search"
            variant="filled"
            size="small"
            onChange={handleSearchTextChange}
            value={searchWord}
          />
          <IconButton>
            <SearchIcon type="submit" onClick={handleSearch}/>
          </IconButton>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List sx = {{ width: "100%"}}>
        {['검색 결과 보기', '추천 여행지 보기', '나의 저장소'].map((text, index) => (
            <React.Fragment key={text}>
              <ListItem button onClick={() => handleClick(index)}>
                <ListItemIcon>
                  <InboxIcon />
                </ListItemIcon>
                <ListItemText primary={text} />
                  <ExpandMore/>
              </ListItem>
              <Collapse in={listOpen[index]} 
                        timeout="auto" 
                        orientation='vertical'
                        unmountOnExit>
                {listOpen[0] === true && <List>
                  {searchResult.length != 0 ? searchResult.map((place) => (
                    <React.Fragment key={place.id}>
                      <PlaceInfo key={place.id} place={place} index={index} reviews={placeReviews} openInfo={setInfoOpen} setSelectedPlace={setSelectedPlace} setPlaceReviews={setPlaceReviews}/>
                    </React.Fragment>  
                  )):<Typography variant='body1'>검색 결과가 없습니다.</Typography>}
                </List>}
                {listOpen[1] === true && <List>
                  {recommendResult.length != 0 ? recommendResult.map((place) => (
                    <React.Fragment key={place.id}>
                      <PlaceInfo key={place.id} place={place} index={index} reviews={placeReviews} openInfo={setInfoOpen} setSelectedPlace={setSelectedPlace} setPlaceReviews={setPlaceReviews}/>
                    </React.Fragment>  
                  )):<Typography variant='body1'>먼저 리뷰를 달아주세요!</Typography>}
                </List>}
                {listOpen[2] === true && <List>
                  {myPlaceResult.length != 0 ? myPlaceResult.map((place) => (
                    <React.Fragment key={place.id}>
                      <PlaceInfo key={place.id} place={place} index={index} reviews={placeReviews} openInfo={setInfoOpen} setSelectedPlace={setSelectedPlace} setPlaceReviews={setPlaceReviews}/>
                    </React.Fragment>  
                  )):<Typography variant='body1'>가고 싶은 장소를 등록해보세요.</Typography>}
                </List>}
                        
              </Collapse>
              <Divider />
            </React.Fragment>
        ))}
            
            
        </List>
      </Drawer>
      <Drawer
        sx={{
          width: drawerWidth+100,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth+100,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="left"
        open={infoOpen}
        
      >
        <DrawerHeader>
          <Box>
            <Typography variant="h5">{selectedPlace.name}</Typography>
          </Box>
          <IconButton onClick={handleInfoDrawerClose}>
            {theme.direction === 'ltr' ? <ClearIcon /> : <ChevronRightIcon />}
          </IconButton>
          
        </DrawerHeader>
        <Divider />
        <Box>
          <Typography variant="subtitle1">{selectedPlace.type} ({selectedPlace.numReviews})  ★{selectedPlace.avgRating}</Typography>
          <Typography variant="subtitle2">{selectedPlace.location}</Typography>
          <Typography variant="caption">{selectedPlace.detail}</Typography>
        </Box>
        <Box
          sx={{
            '& > legend': { mt: 2 },
          }}
        >
          <Typography component="legend">별점</Typography>
          <Rating
            name="simple-controlled"
            value={rating}
            onChange={(event, newRating) => {
              setRating(newRating);
            }}
          />
          <InputBase
            sx={{ ml: 1, flex: 1 }}
            placeholder="리뷰 작성하기"
            inputProps={{ 'aria-label': '리뷰 작성하기' }}
            onChange={handleReviewChange}
          />
          <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
          <IconButton color="primary" sx={{ p: '10px' }} aria-label="directions" onClick={handleSubmit}>
            <DirectionsIcon />
          </IconButton>
        </Box>
        <List sx = {{ width: "100%"}}>
          {placeReviews.map((review) => (
            <React.Fragment key={review.id}>
              <Card sx={{ maxWidth: 345 }}>
                    <CardHeader
                      avatar={
                        <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
                          {review.User.nick[0]}
                        </Avatar>
                      }
                      title={review.User.nick}
                      subheader={review.rating}
                    />
                    <CardContent>
                      <Typography variant="body2" color="text.secondary">
                        {review.content}
                      </Typography>
                    </CardContent>
                    <CardActions disableSpacing>
                      <IconButton aria-label="add to favorites">
                        <FavoriteIcon />
                      </IconButton>
                      <IconButton aria-label="share">
                        <ShareIcon />
                      </IconButton>
                    </CardActions>
              </Card>        
            </React.Fragment>
            
          ))
          }
          
        </List>
      </Drawer>
    </Box>
  );
}
/**
 * <ReviewCard review={review}/>
 * 
 */