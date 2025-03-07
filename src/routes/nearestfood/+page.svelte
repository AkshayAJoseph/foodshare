<script>
  import { getCoords, getDistance, getfoods } from "../../script";

  let selectedValue = $state(0); // Default integer value

  let data;

  const doFetch = async () => {
    data = await getfoods();
    console.log("Before Sorting:", data);
    console.log(data);
    const ucoords = await getCoords();
    const lonu = ucoords.longitude;
    const latu = ucoords.latitude;

    data = data.map((item) => ({
      ...item,
      distance: getDistance(latu, lonu, item.latitude, item.longitude),
    }));

    data.sort((a, b) => a.distance - b.distance);

    console.log("After Sorting:", data);
  };

  doFetch();
</script>

<label> Nearest</label>
