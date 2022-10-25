/* global kakao */

import React, { useEffect, useState, useRef } from 'react';

export default function Map(props) {
    const { markerPositions, size } = props;
    const [kakaoMap, setKakaoMap] = useState(null);
    const [, setMarkers] = useState([]);

    const container = useRef();
    
    useEffect(() => {
        // index.html head에 카카오 API script 추가
        const script = document.createElement("script");
        script.src =
            "https://dapi.kakao.com/v2/maps/sdk.js?appkey=4eb90f589de433bffdfd7f5d82caad00&autoload=false"; //
        document.head.appendChild(script);

        script.onload = () => {
            kakao.maps.load(() => {
                const center = new kakao.maps.LatLng(35.158533, 129.160889)
                const options = {
                    center,
                    level: 4
                };
                const map = new kakao.maps.Map(container.current, options);
                //setMapCenter(center);
                setKakaoMap(map);
            });
        };
    }, [container]);

    useEffect(() => {
        if (kakaoMap == null) {
            return;
        }
        // center 좌표 저장
        const center = kakaoMap.getCenter();

        // viewport size 변경
        //const [width, height] = size;
        const [width, height] = [100, 100];
        container.current.style.width = `${width}vw`;
        container.current.style.height = `${height}vh`;

        // relay out
        kakaoMap.relayout();
        // 원래 center로 설정
        kakaoMap.setCenter(center);
    }, [kakaoMap, size])

    useEffect(() => {
        if (kakaoMap === null) {
            return;
        }

        const positions = markerPositions.map(pos => new kakao.maps.LatLng(...pos))

        setMarkers(markers => {
            // 이전 marker들 지우기
            markers.forEach(marker => marker.setMap(null));

            // 새로운 marker 표시하기
            return positions.map(
                position => new kakao.maps.Marker({ map: kakaoMap, position})
            );
        });

        if (positions.length > 0) {
            const bounds = positions.reduce(
                (bounds, latlng) => bounds.extend(latlng),
                new kakao.maps.LatLngBounds()
            );

            kakaoMap.setBounds(bounds);
        }
    }, [kakaoMap, markerPositions]);

    

    return (
        <div id='myMap' style={{
            width: '100vw',
            height: '100vh',
        }}
        ref = {container} />
    );
}