import {
    createSelector,
    createEntityAdapter
} from "@reduxjs/toolkit";
import { apiSlice } from "../../app/api/apiSlice";

const historiesAdapter = createEntityAdapter()

const initialState = historiesAdapter.getInitialState()

export const historiesApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getHistories: builder.query({
            query: () => '/history',
            transformResponse: responseData => {
                return historiesAdapter.setAll(initialState, responseData)
            },
            providesTags: (result, error, arg) => [
                { type: 'History', id: "LIST" },
                ...result.ids.map(id => ({ type: 'History', id }))
            ]
        })
    })
})

export const {
    useGetHistoriesQuery
} = historiesApiSlice

// returns the query result object
export const selectHistoriesResult = historiesApiSlice.endpoints.getHistories.select()

// Creates memoized selector
const selectHistoriesData = createSelector(
    selectHistoriesResult,
    historiesResult => historiesResult.data // normalized state object with ids & entities
)

//getSelectors creates these selectors and we rename them with aliases using destructuring
export const {
    selectAll: selectAllHistories,
    selectById: selectHistoryById,
    selectIds: selectHistoryIds
    // Pass in a selector that returns the posts slice of state
} = historiesAdapter.getSelectors(state => selectHistoriesData(state) ?? initialState)