import streamlit as st

st.title("MarkDown styles")

codes='''
	```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
'''
st.markdown(codes)

st.markdown(
    '''
    1. first line
    2. second line
    3. third line
    '''
)

st.markdown(
    '''
    - [x] Write the press release
    - [ ] Update the website
    - [ ] Contact the media
    '''
)

st.markdown("That is so funny! :joy:")
st.markdown("That is so funny! :happy:")
st.markdown("That is so funny! :angry:")