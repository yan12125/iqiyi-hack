SWF_NAME=MainPlayer_5_2_28_c3_3_7_5
ABC_INDEX=0
ABC_ID="${SWF_NAME}-${ABC_INDEX}"

rm -rf "${ABC_ID}.abc" "${ABC_ID}/"

abcexport "${SWF_NAME}.swf"
rabcdasm "${ABC_ID}.abc"
pushd "${ABC_ID}/" && patch -p0 -i ../asasm.patch && popd
rabcasm "${ABC_ID}/${ABC_ID}.main.asasm"
abcreplace "${SWF_NAME}.swf" 0 "${ABC_ID}/${ABC_ID}.main.abc"
